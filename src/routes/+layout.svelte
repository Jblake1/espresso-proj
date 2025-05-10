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
    class:s-homepage-background={isHomepage}
    class:s-otherpages-background={!isHomepage}
/>

<main class="relative z-10">
    <slot />
</main>

<style lang="postcss">
    /*
     This :global(body) rule applies unconditional base styles from within this layout.
     Alternatively, ALL such base styles could live in '../app.postcss'.
     If styles in 'app.postcss' already set these, you might not need this block,
     or you might use it to layer layout-specific base styles on top.
    */
    :global(body) {
        @apply min-h-screen w-full m-0 p-0 font-sans; /* Your base Tailwind classes */
        /* Add any other truly global, unconditional body styles here if not in app.postcss */
    }

    :global(body.s-homepage-background) {
        /* Styles exclusively for the homepage background.
           Corrected path for image in 'static/images/': /images/... */
        @apply bg-[url('/images/christina-bi-Vgm0CSJeU14-unsplash.jpg')] bg-cover bg-center bg-no-repeat bg-fixed;
    }

    :global(body.s-otherpages-background) {
        /* Fallback background styles for pages that are NOT the homepage */
        @apply bg-gray-100; /* Your existing Tailwind class for other pages */
        /* To ensure no background image from homepage styles bleeds through if classes somehow overlapped
           or if you want to be very explicit (though the logic here makes them mutually exclusive): */
        /* background-image: none; */
    }
</style>