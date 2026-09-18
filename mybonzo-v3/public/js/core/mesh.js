export class MeshCore {
    constructor() {
        this.status = 'initializing';
    }
    async checkStatus() {
        try {
            const response = await fetch('/api/mesh/status');
            return await response.json();
        } catch (e) {
            return { status: 'offline' };
        }
    }
}