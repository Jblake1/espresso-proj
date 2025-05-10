
<script lang="ts">
    import { onMount } from 'svelte';

    let drink = $state('');
</script>


<style>


</style>

<!-- bg-hero-pattern bg-cover bg-center -->
<div class="min-h-screen flex justify-center items-center">
    <form class="h-screen w-1/2 md:w-1/3 flex flex-col justify-start items-center pt-10 mx-auto">
        <h2 class="label-wrapper min-w-40 min-h-6 text-center">
            <label for="drink" class="label__lg font-semibold">What are we brewing today?</label>
        </h2>
        <select bind:value={drink} id="drink" class="select w-full px-3 py-2 border rounded min-h-10 min-w-30">
            <option value="">Select a drink</option>
            <option value="Espresso">Espresso</option>
            <option value="Coffee">Coffee</option>
        </select>
    </form>
</div>