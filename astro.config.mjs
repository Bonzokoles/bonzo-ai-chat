import { defineConfig } from 'astro/config';
import react from '@astrojs/react';

// Electron desktop app - static build
// For Cloudflare deployment, switch to 'server' with cloudflare adapter
export default defineConfig({
    output: 'static',
    integrations: [react()],
    vite: {
        ssr: {
            external: ['node:async_hooks']
        }
    },
    build: {
        inlineStylesheets: 'auto'
    }
});
