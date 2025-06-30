// Load Vega scripts from CDN
const loadScript = (src) => {
    return new Promise((resolve, reject) => {
        const script = document.createElement('script');
        script.src = src;
        script.onload = resolve;
        script.onerror = reject;
        document.head.appendChild(script);
    });
};

// Load Vega libraries sequentially to ensure proper initialization
window.vegaReady = (async () => {
    try {
        // First load Vega core and wait for it to complete
        await loadScript('https://cdn.jsdelivr.net/npm/vega@5.25.0/build/vega.js');

        // Then load Vega-Lite after Vega is available
        await loadScript('https://cdn.jsdelivr.net/npm/vega-lite@5.16.0/build/vega-lite.js');

        // Finally load Vega-Embed
        await loadScript('https://cdn.jsdelivr.net/npm/vega-embed@6.22.1/build/vega-embed.js');

        // Ensure global objects are properly initialized
        if (!window.vega) {
            throw new Error('Vega failed to initialize');
        }

        return true;
    } catch (error) {
        console.error('Failed to load Vega libraries:', error);
        throw error;
    }
})();