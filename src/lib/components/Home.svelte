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

  
  onMount(() => autofocus && nameEl.focus && nameEl.focus())    // if autofocus is true, we run nameEl.focus()

</script>

<style>

  :global(.recent-setups) {
      margin: 0;
      padding: 0;
    }

  .visible-heading {
  display: flex;
  visibility: visible !important;
  opacity: 1 !important;
  color: black !important;
  font-size: 1.2em !important;
  margin-top: 1em !important;
  flex-direction: column; /* Arrange elements in a row */
  align-items: flex-start; /* Align items at the top */
  gap: 10px;
  }

  .outerContainer {
      display: flex;
      flex-direction: row; /* Arrange elements in a row */
      align-items: flex-start; /* Align items at the top */
      gap: 10px; /* Add spacing between form and RecentSetups */
    }


  .innerContainer {
    display: flex;
    flex-direction: column; /* Stack elements vertically */
    align-items: flex-start; /* Align items at the top */
    gap: 10px; /* Add spacing between form elements */
    width: 50%; /* Make form take 50% of the width */
  }


  .toDoForm {
    flex: 0.7; /* Take up all available space */
    margin-right: 0;
  }

  .RecentSetups {
    flex: 0.3; /* Take up all available space */
    margin-right: 0;
  }

  .CoffeeSetupSave {
    flex: 1; /* Take up all available space */
    margin-right: 0;
  }

</style>

<h1>Home</h1>

<div class="outerContainer">
  <div class="innerContainer">
    <form class = "toDoForm">
      <h2 class="label-wrapper">
        <label for="drink" class="label__lg">Drink</label>
      </h2>
      <input bind:value={drink} bind:this={drinkEl} use:selectOnFocus 
        type="text" id="drink" autoComplete="off" class="input input__lg" 
      />

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

      <!-- <h1 class="visible-heading">
        Bean Description:{beanDescription}
      </h1> -->

      
        
      <h1 class="visible-heading">
        Grind Segment:{grindSegment}
      </h1>

      <h1 class="visible-heading">
        Grind Setting:{grindSetting}
      </h1>
      
      
      <button type="submit" disabled={false} class="btn btn__primary btn__lg" onclick={submit} >Submit</button>

    </form>

    <div class="CoffeeSetupSave">
      <CoffeeSetupSave bind:value={messageBind} props={snapPropData}/>
    </div>
  </div>

  <div class="RecentSetups">
    <RecentSetups props={snapPropData} trigger={messageBind}/>
  </div>
</div>
