<script lang="ts">
    
    import { storePopup } from '@skeletonlabs/skeleton';
    import { computePosition, autoUpdate, offset, shift, flip, arrow } from '@floating-ui/dom';
    import * as popup from '@floating-ui/dom';
    import '../app.postcss';

    storePopup.set({ computePosition, autoUpdate, offset, shift, flip, arrow });
    
</script>
  
<slot />