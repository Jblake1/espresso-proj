<script lang="ts">
    
    import { storePopup } from '@skeletonlabs/skeleton';
    import { page } from '$app/stores';
    import { computePosition, autoUpdate, offset, shift, flip, arrow } from '@floating-ui/dom';
    import * as popup from '@floating-ui/dom';
    import '../app.postcss';

    storePopup.set({ computePosition, autoUpdate, offset, shift, flip, arrow });

    $: isHomepage = $page.route.id === '/';

    $: {
        if ($page.route.id !== undefined) { // Log only when route.id is available
            console.log('Current $page.route.id:', $page.route.id);
            console.log('Calculated isHomepage:', isHomepage);
        }
    }
    
</script>
  
<svelte:body
    class:test-always-on-body={true}
    class:test-homepage-only-body={isHomepage}
/>

<main class="relative z-10">
    <slot />
</main>

<style lang="postcss">
    /* Base body styles (can also be in app.postcss) */
    :global(body) {
        @apply min-h-screen w-full m-0 p-0 font-sans;
    }

    /* Styles for testing if the classes get applied */
    :global(body.test-always-on-body) {
        border: 10px solid limegreen !important; /* Very visible */
    }
    :global(body.test-homepage-only-body) {
        outline: 10px solid dodgerblue !important; /* Very visible */
    }

    /* Comment out your actual background image styles for this test */
    /*
    :global(body.s-homepage-background) {
        @apply bg-[url('/images/christina-bi-Vgm0CSJeU14-unsplash.jpg')] bg-cover bg-center bg-no-repeat bg-fixed;
    }
    :global(body.s-otherpages-background) {
        @apply bg-gray-100;
    }
    */
</style>