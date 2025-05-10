<script lang="ts">
    
    import { storePopup } from '@skeletonlabs/skeleton';
    import { page } from '$app/stores';
    import { computePosition, autoUpdate, offset, shift, flip, arrow } from '@floating-ui/dom';
    import * as popup from '@floating-ui/dom';
    import '../app.postcss';

    storePopup.set({ computePosition, autoUpdate, offset, shift, flip, arrow });

    $: isHomepage = $page.route.id === '/';

    // Reactive classes for the wrapper div
    let dynamicWrapperClasses = '';
    $: {
        // Base classes for the wrapper on all pages
        const baseClasses = 'min-h-screen w-full transition-colors duration-300 ease-in-out';

        if (isHomepage) {
            // Classes for the homepage (using your pre-defined Tailwind bg image)
            dynamicWrapperClasses = `${baseClasses} bg-hero-pattern bg-cover bg-center bg-no-repeat bg-fixed`;
        } else {
            // Classes for other pages (e.g., a Skeleton surface color or a simple Tailwind color)
            dynamicWrapperClasses = `${baseClasses} bg-surface-100-800-token`; // Example Skeleton surface
            // Or a simple Tailwind color: dynamicWrapperClasses = `${baseClasses} bg-gray-100`;
        }
        // For debugging in browser console:
        // console.log('Applied dynamicWrapperClasses:', dynamicWrapperClasses);
    }
</script>

<div class="{dynamicWrapperClasses}">
    <main class="relative z-10">
        <slot />
    </main>
</div>

<style lang="postcss">
    /*
      Ensure html and body allow the wrapper div to truly take up full height.
      Skeleton's app.postcss and theme usually handle this, but good to be aware.
      If Skeleton sets a background on <body>, this wrapper div's background will sit on top.
    */
    :global(html), :global(body) {
        height: 100%; /* Or min-height: 100% if preferred */
        margin: 0;
        padding: 0;
    }

    /*
      Any truly global font settings or base text colors from Skeleton
      will likely apply through app.postcss to the body and be inherited.
      If you needed to override something specific here, you could.
    */
</style>