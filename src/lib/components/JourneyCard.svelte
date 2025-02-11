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

    // Creates a card shape with the following fields
    // Grind Setting Field nullable
    // Shot time nullable
    // notes nullable
    // date not nullable
    
    let datePosted = $state('');
    let notes = $state('');
    let grindSetting = $state('');
    let shotTime = $state('');
    let journeyID = $state('');
    let cardID = $state('');

    const createJourneyCard = async () => {
        try {
            const response = await fetch('http://localhost:4000/journeyCard', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    journeyID: props.journeyData.journeyID
            })
        });

            if (!response.ok) {
                throw new Error('Network response of journeyCard not ok');
            }
            
        } catch (err) {
            console.error('Error getting journey:', err);
            alert('An error occurred while posting the journey card.');
        }
    }

    const displayJourneyCard = async () => {
        try {
            const response = await fetch('http://localhost:4000/journeyCard', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            });
            
            // 
            // Investigate data flow of Journey id. Do integers behave diffferently
            // or is the id column in journey blank. Or is the foreign id not generating
            if (response.ok) {
                const data = await response.json();
                console.log('JourneyCards:', data);
                const journeyCards = data.journeyCards;
                console.log('JourneyCardsData:', journeyCards);

                if (journeyCards.length > 0) {
                    // Destructure the first setup object
                    cardID = journeyCards[0].id;
                    datePosted = journeyCards[0].datePosted;
                    notes = journeyCards[0].notes;
                    grindSetting = journeyCards[0].grindSetting;
                    shotTime = journeyCards[0].shotTime;
                    journeyID = journeyCards[0].journey_id;
                }
            }
        } catch (err) {
            console.error('Error getting journey:', err);
            alert('An error occurred while getting the journey.');
        }
    };

    const updateJourneyCard = async () => {
        try {
            const response = await fetch('http://localhost:4000/journeyCardEdit', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    id: cardID,
                    grindSetting: grindSetting,
                    shotTime: shotTime,
                    datePosted: datePosted,
                    notes: journeyID
                })
            });

            if (!response.ok) {
                throw new Error('Network response of journeyCard update not ok');
            }

            } catch (err) {
            console.error('Error getting journey:', err);
            alert('An error occurred while updating card.');
        }
    };

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
        <p class="card_text">card{cardID}</p>
        <p class="card_text">date posted: {datePosted}</p>
        <p class="card_text">{grindSetting}</p>
        <p class="card_text">{shotTime}</p>
        <p class="card_text">{notes}</p>
        <p class="card_text">Journey id: {journeyID}</p>
        <div class="tabButton">
            <button onclick={()=>updateJourneyCard()}>Update</button>
        </div>
    </div>
</div>