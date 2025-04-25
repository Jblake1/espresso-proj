<!-- homepage where espresso inputs are submitted 
 and setups can be saved to a intermediary db -->
<script lang='ts'>
  import { onMount } from 'svelte'
  import { selectOnFocus } from '../actions'
  import CoffeeSetupSave from './CoffeeSetupSave.svelte';
  import RecentSetups from './RecentSetups.svelte';
  import { writable } from 'svelte/store';

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

    // Get access to the user store
    const userStore = writable(null);

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
      const response = await fetch('/recommendation', {
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
  
  // Load user data from localStorage on component mount
  onMount(() => {
    const storedUser = localStorage.getItem('user');
    if (storedUser) {
      try {
        userStore.set(JSON.parse(storedUser));
      } catch (e) {
        console.error("Error parsing localStorage user data:", e);
      }
    }
  });

</script>

<style>
  /* Keep global styles */
  :global(.recent-setups) {
    margin: 0;
    padding: 0;
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
<div class="flex flex-col items-start gap-4 p-4 md:flex-row md:gap-6 md:p-6">
  <div class="flex flex-col items-start gap-4 p-4">
    <form class="toDoForm">
      <div class="flex flex-row md:flex-col items-start gap-4 p-4">
        <div class="flex flex-col items-start gap-4 px-4">
          <h2 class="label-wrapper mb-1 min-w-40 min-h-6">
            <label for="drink" class="label__lg font-semibold">Drink</label>
          </h2>
          <select bind:value={drink} id="drink" class="select w-full px-3 py-2 border rounded min-h-10 min-w-40">
            <option value="">Select a drink</option>
            <option value="Espresso">Espresso</option>
            <option value="Coffee">Coffee</option>
          </select>

          <h2 class="label-wrapper min-w-40 min-h-6">
            <label for="brewing_device" class="label__lg font-semibold">Brewing Device</label>
          </h2>
          <select bind:value={brewingDevice} id="brewingDevice" class="select w-full px-3 py-2 border rounded min-w-40 min-h-10" disabled={!drink}>
            <option value="">Select a device</option>
            {#each deviceOptions as device}
              <option value={device}>{device}</option>
            {/each}
          </select>
        </div>
        <div class="flex flex-col items-start gap-4 px-4">
          <h2 class="label-wrapper min-w-40 min-h-6">
            <label for="grinder" class="label__lg font-semibold">Grinder</label>
          </h2>
          <select bind:value={grinder} id="grinder" class="select w-full px-3 py-2 border rounded min-w-40 min-h-10" disabled={!drink}>
            <option value="">Select a grinder</option>
            {#each grinderOptions as grinder}
              <option value={grinder}>{grinder}</option>
            {/each}
          </select>

          <h2 class="label-wrapper min-w-40 min-h-6">
            <label for="coffeeBeans" class="label__lg font-semibold">Bean</label>
          </h2>
          <div class="relative w-full">
            <input bind:value={coffeeBeans} bind:this={coffeeBeansEl} use:selectOnFocus 
              type="text" id="coffeeBeans" autoComplete="off" class="input input__lg min-w-40 min-h-10"
              maxlength="40" placeholder="Enter coffee bean" 
            />
            <div class="text-xs text-gray-500 absolute right-2 bottom-6">
              {coffeeBeans.length}/40
            </div>
          </div>
        </div>
      </div>
      {#if $userStore}
        <button 
          type="button" class="btn variant-filled" onclick={submit} disabled={isSubmitting}>
          {#if isSubmitting}
            Submitting...
          {:else}
            Submit
          {/if}
        </button>
      {:else}
      <div></div>
      {/if}
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

  {#if $userStore} <!-- Check if user is authenticated -->
    <div class="RecentSetups">
      <RecentSetups props={snapPropData} trigger={messageBind}/>
    </div>
  {:else}
    <div class="w-full text-center p-10 border border-primary-200 rounded-lg bg-tertiary-900/50">
      <p class="text-xl font-semibold text-tertiary-200">Not Logged In</p>
      <p class="mt-2 text-tertiary-400">No coffee records can be displayed</p>
      <a href="/login" class="btn variant-filled-primary mt-6">Login to view</a>
    </div>
  {/if}
</div>
