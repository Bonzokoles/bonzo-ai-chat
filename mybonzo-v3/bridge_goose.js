import { exec } from 'child_process';
import fs from 'fs';

const ACCOUNT_ID = "7f490d58a478c6baccb0ae01ea1d87c3";
const DB_ID = "84f0f3cb-7778-4cc4-a6ba-e823ef52f1f3";
// Goose ma dostęp do zmiennej środowiskowej
const API_TOKEN = process.env.CLOUDFLARE_API_TOKEN;

async function checkQueue() {
    console.log("Checking Agent Mesh Queue...");
    try {
        const query = "SELECT * FROM tasks WHERE status = 'pending' LIMIT 1";
        const res = await fetch(`https://api.cloudflare.com/client/v4/accounts/${ACCOUNT_ID}/d1/database/${DB_ID}/query`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${API_TOKEN}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ sql: query })
        });
        const data = await res.json();
        
        if (data.result?.[0]?.results?.length > 0) {
            const task = data.result[0].results[0];
            console.log("RECEIVED TASK:", task.instruction);
            executeTask(task);
        }
    } catch (e) { console.error("Polling Error", e); }
}

function executeTask(task) {
    // Goose/PowerShell execution bridge
    console.log(`EXECUTING: ${task.instruction}`);
    exec(task.instruction, async (error, stdout, stderr) => {
        const result = stdout || stderr || error?.message;
        const status = error ? 'failed' : 'completed';
        
        // Odesłanie wyniku do chmury
        await fetch(`https://api.cloudflare.com/client/v4/accounts/${ACCOUNT_ID}/d1/database/${DB_ID}/query`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${API_TOKEN}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                sql: "UPDATE tasks SET status = ?, result = ? WHERE id = ?",
                params: [status, result, task.id]
            })
        });
        console.log("TASK FINISHED & UPDATED IN MESH.");
    });
}

// Interwał sprawdzania (co 5 sekund)
setInterval(checkQueue, 5000);
console.log("GOOSE_BRIDGE ACTIVE. Listening for commands from MyBonzo.com...");