
<script lang="ts">
    import { onMount } from 'svelte';

    let drink = $state('');
</script>


<style>


</style>

<!-- bg-hero-pattern bg-cover bg-center -->
<div class="min-h-screen flex flex-col justify-start items-center p-4">
    <form class="w-full max-w-sm flex flex-col items-center space-y-6 p-6 md:p-8 bg-white shadow-xl rounded-lg">
        <div class="text-center"> <label for="drink" class="text-xl md:text-2xl font-semibold text-gray-800">
                What are we brewing today?
            </label>
        </div>

        <select bind:value={drink} id="drink" class="select w-full px-4 py-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-base">
            <option value="" disabled>Select a drink</option> <option value="Espresso">Espresso</option>
            <option value="Coffee">Coffee</option>
        </select>

        </form>
</div>