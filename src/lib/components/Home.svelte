<!-- Placeholder -->
<script lang="ts">
    import { onMount } from 'svelte';

    let drink = $state('');
</script>


<style>


</style>

<form class="h-screen w-full bg-hero-pattern bg-cover bg-center flex justify-center items-center">
    <h2 class="label-wrapper min-w-40 min-h-6">
        <label for="drink" class="label__lg font-semibold">What are we brewing today?</label>
    <select bind:value={drink} id="drink" class="select w-full px-3 py-2 border rounded min-h-10 min-w-30">
        <option value="">Select a drink</option>
        <option value="Espresso">Espresso</option>
        <option value="Coffee">Coffee</option>
      </select>
</form>