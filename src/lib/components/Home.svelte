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

  let canvas;

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
      <input bind:value={brewingDevice} bind:this={brewingDeviceEl} use:selectOnFocus 
        type="text" id="brewingDevice" autoComplete="off" class="input input__lg" 
      />

      <h2 class="label-wrapper">
        <label for="grinder" class="label__lg">Grinder</label>
      </h2>
      <input bind:value={grinder} bind:this={grinderEl} use:selectOnFocus 
        type="text" id="grinder" autoComplete="off" class="input input__lg" 
      />

      <h2 class="label-wrapper">
        <label for="coffeeBeans" class="label__lg">Bean</label>
      </h2>
      <input bind:value={coffeeBeans} bind:this={coffeeBeansEl} use:selectOnFocus 
        type="text" id="coffeeBeans" autoComplete="off" class="input input__lg" 
      />
      
      <!-- Keep original button classes exactly as they were -->
      <button type="button" class="btn variant-filled" onclick={submit}>Submit</button>
    </form>

    <div class="CoffeeSetupSave">
      <CoffeeSetupSave bind:value={messageBind} props={snapPropData}/>
    </div>
  </div>

  <div class="RecentSetups">
    <RecentSetups props={snapPropData} trigger={messageBind}/>
  </div>
</div>
