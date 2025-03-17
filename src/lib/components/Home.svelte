<!-- homepage where espresso inputs are submitted 
 and setups can be saved to a intermediary db -->
<script lang='ts'>
  import { onMount } from 'svelte'
  import { selectOnFocus } from '../actions'
  import CoffeeSetupSave from './CoffeeSetupSave.svelte';
  import RecentSetups from './RecentSetups.svelte';

  const { autofocus } = $props<{ autofocus: boolean }>()

  let name = $state('');
  let brewingDevice = $state('');
  let brewTime = $state('');
  let drink = $state('');
  let grinder = $state('');
  let grindSetting = $state('');
  let grindSegment = $state('');
  let coffeeBeans = $state('');
  let advice = $state('');
  let beanDescription = $state('');
  let snapPropData = $state({});
  let formErrors = $state('');
  let isSubmitting = $state(false);

  let espressoDevices = [
    "Espresso Machine", 
    "AeroPress", 
    "Moka Pot",
    "Lever Machine"
  ];
  
  let coffeeDevices = [
    "Pour Over", 
    "French Press", 
    "Drip Machine",
    "Cold Brew"
  ];

  let coffeeGrinders = [
    "DF 54", 
    "DF 64",
    "Baratza Encore",
    "Baratza Encore ESP",
    "Baratza Virtuoso",
    "Breville Smart Grinder Pro",
    "1Zpresso JX Pro"
  ];

  let espressoGrinders = [
    "DF 54", 
    "DF 64",
    "Baratza Encore",
    "Baratza Encore ESP",
    "Baratza Sette 270",
    "Baratza Virtuoso",
    "Breville Smart Grinder Pro",
    "Eureka Mignon Specialita",
    "1Zpresso JX Pro"
  ];

  // Create a reactive variable that updates when drink changes
  let deviceOptions = $derived(
  drink === "Espresso" ? espressoDevices : 
  drink === "Coffee" ? coffeeDevices : []
  );

  let grinderOptions = $derived(
  drink === "Espresso" ? espressoGrinders : 
  drink === "Coffee" ? coffeeGrinders : []
  );

  // Using $effect to reset brewing device when drink changes
  $effect(() => {
    if (drink) {
      brewingDevice = "";  // Clear the brewing device when drink changes
    }
  });

  let messageBind = $state('');

  let snapProp = () => ({
    drink: drink,
    brewingDevice: brewingDevice,
    coffeeBeans: coffeeBeans,
    grinder: grinder,
    grindSetting: grindSetting
  });

  let nameEl: HTMLInputElement;
  let brewingDeviceEl: HTMLInputElement;
  let drinkEl: HTMLInputElement;
  let grinderEl: HTMLInputElement;
  let coffeeBeansEl: HTMLInputElement; 


  const submit = async () => {
     // Reset error message
     formErrors = '';
    
    // Validate all required fields
    if (!drink) {
      formErrors = 'Please select a drink type';
      return;
    }
    
    if (!brewingDevice) {
      formErrors = 'Please select a brewing device';
      return;
    }
    
    if (!grinder) {
      formErrors = 'Please select a grinder';
      return;
    }
    
    if (!coffeeBeans || coffeeBeans.trim() === '') {
      formErrors = 'Please enter coffee bean information';
      return;
    }

    // Proceed with submission if all validations pass
    isSubmitting = true;

    try {
      const response = await fetch('http://localhost:4000/recommendation', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          brewing_device: brewingDevice,
          drink,
          grinder,
          coffee_beans: coffeeBeans
        })
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      } else {
        const data = await response.json();
        console.log('Received data:', data);
        const advice = data.advice;
        console.log('Advice:', advice);
        grindSetting = advice.grind_recommendation; // Extract grind setting
        grindSegment = advice.bean_segmentation; // Extract grind segmentation
        console.log('Grind Segment:', grindSegment);
        beanDescription = advice.bean_analysis; // Extract bean description
        console.log('Bean Description:', beanDescription);
        snapPropData = snapProp();
        

      }
    } catch (error) {
      console.error('There was a problem with the fetch operation:', error);
      formErrors = 'Error submitting data. Please try again.';
    } finally {
      isSubmitting = false;
    }
  }
  

  const onCancel = () => {
    name = ''
    brewingDevice = '';
    drink = '';
    grinder = '';
    coffeeBeans = '';
    advice = '';
    brewTime = '';
    grindSetting = '';
    grindSegment = '';
    beanDescription = '';
    nameEl.focus()            // give focus to the name input
  }

  
  onMount(() => autofocus && nameEl.focus && nameEl.focus());    // if autofocus is true, we run nameEl.focus()
  

</script>

<style>
  /* Keep global styles */
  :global(.recent-setups) {
    margin: 0;
    padding: 0;
  }


  /* Update container classes with Tailwind */
  .outerContainer {
    @apply flex flex-row items-start gap-6 p-6;
  }

  .innerContainer {
    @apply flex flex-col items-start gap-4 w-1/5 p-4; /* Changed from w-2/5 to w-1/5 */
  }

  .toDoForm {
    @apply flex-[0.7] mr-0 w-full p-4;
  }

  /* Keep label-wrapper but add padding */
  .label-wrapper {
    @apply mb-2 pl-1;
  }

  /* Add styling to inputs without changing class names */
  .input__lg {
    @apply w-full px-3 py-2 mb-4 border rounded;
  }

  /* Keep original classes intact */
  .RecentSetups {
    @apply flex-[0.3] mr-0 p-4 pl-8 ; /* Added pl-8 for left padding */
  }
  
  .CoffeeSetupSave {
    @apply flex-1 mr-0 p-4 rounded;
  }

  /* Don't modify btn and variant-filled as they might be from a component library */
</style>

<!-- HTML remains exactly the same -->
<div class="outerContainer">
  <div class="innerContainer">
    <form class="toDoForm">
      <h2 class="label-wrapper">
        <label for="drink" class="label__lg">Drink</label>
      </h2>
      <select bind:value={drink} id="drink" class="select w-full px-3 py-2 mb-4 border rounded">
        <option value="">Select a drink</option>
        <option value="Espresso">Espresso</option>
        <option value="Coffee">Coffee</option>
      </select>

      <h2 class="label-wrapper">
        <label for="brewing_device" class="label__lg">Brewing Device</label>
      </h2>
      <select bind:value={brewingDevice} id="brewingDevice" class="select w-full px-3 py-2 mb-4 border rounded" disabled={!drink}>
        <option value="">Select a device</option>
        {#each deviceOptions as device}
          <option value={device}>{device}</option>
        {/each}
      </select>

      <h2 class="label-wrapper">
        <label for="grinder" class="label__lg">Grinder</label>
      </h2>
      <select bind:value={grinder} id="grinder" class="select w-full px-3 py-2 mb-4 border rounded" disabled={!drink}>
        <option value="">Select a grinder</option>
        {#each grinderOptions as grinder}
          <option value={grinder}>{grinder}</option>
        {/each}
      </select>

      <h2 class="label-wrapper">
        <label for="coffeeBeans" class="label__lg">Bean</label>
      </h2>
      <div class="relative w-full">
        <input bind:value={coffeeBeans} bind:this={coffeeBeansEl} use:selectOnFocus 
          type="text" id="coffeeBeans" autoComplete="off" class="input input__lg" 
          maxlength="40" placeholder="Enter coffee bean" 
        />
        <div class="text-xs text-gray-500 absolute right-2 bottom-6">
          {coffeeBeans.length}/40
        </div>
      </div>
      
      <!-- Keep original button classes exactly as they were -->
      <button 
        type="button" class="btn variant-filled" onclick={submit} disabled={isSubmitting}>
        {#if isSubmitting}
          Submitting...
        {:else}
          Submit
        {/if}
      </button>
    </form>

    {#if formErrors}
      <div class="text-red-500 mb-4 p-2 bg-red-100 border border-red-300 rounded">
        {formErrors}
      </div>
    {/if}

    <div class="CoffeeSetupSave">
      <CoffeeSetupSave bind:value={messageBind} props={snapPropData}/>
    </div>
  </div>

  <div class="RecentSetups">
    <RecentSetups props={snapPropData} trigger={messageBind}/>
  </div>
</div>
