<!-- components/NewTodo.svelte -->
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

  // let snapProp = $state({
  //   drink: "es",
  //   brewingDevice: "brewingDevice",
  //   coffeeBeans: "coffeeBeans",
  //   grinder: "grinder",
  //   grindSetting: "grindSetting"
  // });
  
  //LOOK FOR FIX TO REFERENCING SELF REFERENCE STATE
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
      }

      const data = await response.json();
      console.log('Received data:', data);
      const advice = data.advice;
      console.log('Advice:', advice);
      grindSetting = advice.grind_recommendation; // Extract grind setting
      grindSegment = advice.bean_segmentation; // Extract grind segmentation
      console.log('Grind Segment:', grindSegment);
      beanDescription = advice.bean_analysis; // Extract bean description
      console.log('Bean Description:', beanDescription);
      snapPropData = snapProp()
    ;

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

  .outer-container {
      display: flex;
      flex-direction: row; /* Arrange elements in a row */
      align-items: flex-start; /* Align items at the top */
      gap: 10px; /* Add spacing between form and RecentSetups */
    }


  .inner-container {
    display: flex;
    flex-direction: column; /* Stack elements vertically */
    align-items: flex-start; /* Align items at the top */
    gap: 10px; /* Add spacing between form elements */
    width: 50%; /* Make form take 50% of the width */
  }


  .toDoForm {
    width: 50%
  }

  .RecentSetups {
    width: 50%; 
  }

  .CoffeeSetupSave {
    width: 50%;
  }

</style>


<div class="outer-container">
  <div class="inner-container">
    <form class = "toDoForm">
      <h2 class="label-wrapper">
        <label for="drink" class="label__lg">Drink</label>
      </h2>
      <input bind:value={drink} bind:this={drinkEl} use:selectOnFocus 
        type="text" id="drink" autoComplete="off" class="input input__lg" 
      />

      <h2 class="label-wrapper">
        <label for="brewing_device" class="label__lg">Model</label>
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
      <CoffeeSetupSave drink={snapPropData}/>
    </div>
  </div>

  <div class="RecentSetups">
    <RecentSetups />
  </div>

</div>
