<!-- recieve journey id from svelte
    return list of journey cards
    iterate through list of journey cards
    display each journey card (up to 3)
    indicate if there are more cards and count how many 
    add a button to view more cards
    make some field on cards editable (edits update in db)
     -->

<script lang="ts">
    import { onMount } from "svelte";

    // Props that can be passed from the parent Archive component
    let props = $props();

    let title = '';
    let date = '';
    let notes = '';
    let grindSetting = '';
    let iteration = '';
    let journeyID = '';

    const createJourneyCard = async () => {
        try {
            const response = await fetch('http://localhost:4000/postJourneyCard', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            if (response.ok) {
                const data = await response.json();
                console.log('Journey:', data);
                const journeys = data.journeys;
                console.log('journeys:', journeys);

                if (journeys.length > 0) {
                    // Destructure the first setup object
                    title = journeys[0].title;
                    date = journeys[0].date;
                    notes = journeys[0].notes;
                    grindSetting = journeys[0].grindSetting;
                    iteration = journeys[0].iteration;
                    journeyID = journeys[0].journeyID;
                }
            }
        } catch (err) {
            console.error('Error getting journey:', err);
            alert('An error occurred while getting the journey.');
        }
    }

    const displayJourneyCard = async () => {
        try {
            const response = await fetch('http://localhost:4000/getJourneyCard', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            if (response.ok) {
                const data = await response.json();
                console.log('Journey:', data);
                const journeys = data.journeys;
                console.log('journeys:', journeys);

                if (journeys.length > 0) {
                    // Destructure the first setup object
                    title = journeys[0].title;
                    date = journeys[0].date;
                    notes = journeys[0].notes;
                    grindSetting = journeys[0].grindSetting;
                    iteration = journeys[0].iteration;
                    journeyID = journeys[0].journeyID;
                }
            }
        } catch (err) {
            console.error('Error getting journey:', err);
            alert('An error occurred while getting the journey.');
        }
    }
    
    onMount(() => {
        displayJourneyCard();
    });
</script>

<style>
    .journey-card {
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1rem;
        background-color: white;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    h3 {
        margin: 0 0 0.5rem 0;
        color: #333;
    }

    .card_text {
        font-size: 0.9rem;
        color: #666;
        margin: 0 0 0.5rem 0;
    }

    .tabButton {
        background-color: #f1f1f1;
        border: none;
        color: black;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
    }

</style>

<div class="outerContainer">
    <div class="tabButton">
        <button onclick={()=>createJourneyCard()}>+</button>
    </div>

    <div class="journey-card">
        <h3>{title}</h3>
        <p class="card_text">{date}</p>
        <p class="card_text">{grindSetting}</p>
        <p class="card_text">{notes}</p>
        <p class="card_text">Iteration: {iteration}</p>
        <p class="card_text">journey: {journeyID}</p>
    </div>
</div>