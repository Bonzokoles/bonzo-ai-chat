undefined
export const createMoaControl = () => {
    return `
        <div class="agent-card" style="border: 1px solid var(--accent-yellow); background: rgba(255, 204, 0, 0.02);">
            <div class="panel-header" style="color: var(--accent-yellow)">Darmowy_Obieg_MOA</div>
            <div style="font-size: 0.6rem; color: #666; margin-bottom: 10px;">Łańcuch: CF -> GROQ -> GEMINI</div>
            <button onclick="runMoaTask()" style="width: 100%; font-size: 0.7rem; border-color: var(--accent-yellow); color: var(--accent-yellow);">ACTIVATE_FREE_CHAIN</button>
        </div>
    `;
};