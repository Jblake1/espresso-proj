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
    let cardData = $state([
        { datePosted: '', notes: '', grindSetting: '', shotTime: '', cardID: '', journeyID: '', iteration: '' },
        { datePosted: '', notes: '', grindSetting: '', shotTime: '', cardID: '', journeyID: '', iteration: '' },
        { datePosted: '', notes: '', grindSetting: '', shotTime: '', cardID: '', journeyID: '', iteration: '' },
        { datePosted: '', notes: '', grindSetting: '', shotTime: '', cardID: '', journeyID: '', iteration: '' }
    ]);

    


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
            displayJourneyCard(props.journeyData.journeyID);
            
        } catch (err) {
            console.error('Error getting journey:', err);
            alert('An error occurred while posting the journey card.');
        }
    }

    const deleteJourneyCard = async (cardID, index) => {
        try {
            const response = await fetch('http://localhost:4000/journeyCardDelete', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    id: cardID
                })
            });

            if (!response.ok) {
                throw new Error('Network response of journeyCard delete not ok');
            }

            cardData[index].cardID = '';
            cardData[index].datePosted = '';
            cardData[index].iteration = '';
            cardData[index].notes = '';
            cardData[index].grindSetting = '';
            cardData[index].shotTime = '';
            cardData[index].journeyID = '';
            
        } catch (err) {
            console.error('Error getting journey:', err);
            alert('An error occurred while deleting the journey card.');
        }
    };

    const displayJourneyCard = async (journeyData) => {
        try {
            console.log(`Sending journeyID: ${journeyData}`);
            const response = await fetch(`http://localhost:4000/journeyCard?journeyID=${journeyData}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            });
            
            
            if (response.ok) {
                const data = await response.json();
                console.log('JourneyCards:', data);
                const journeyCards = data.journeyCards;
                console.log('JourneyCardsData:', journeyCards);

                journeyCards.forEach((card, index) => {
                    if (index < cardData.length) {
                        
                        cardData[index].cardID = card.id;
                        cardData[index].datePosted = card.datePosted;
                        cardData[index].iteration = card.iteration;
                        cardData[index].notes = card.notes;
                        cardData[index].grindSetting = card.grindSetting;
                        cardData[index].shotTime = card.shotTime;
                        cardData[index].journeyID = props.journeyData.journeyID;
                    }
                });
            }
        } catch (err) {
            console.error('Error getting journey:', err);
            alert('An error occurred while getting the journey.');
        }
    };

    const updateJourneyCard = async (index) => {
        try {
            const response = await fetch('http://localhost:4000/journeyCardEdit', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    id: cardData[index].cardID,
                    grindSetting: cardData[index].grindSetting,
                    shotTime: cardData[index].shotTime,
                    notes: cardData[index].notes
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

    // Function to format date to mm/dd/yy
    function formatDate(dateString) {
        if (!dateString) return '';
        
        const date = new Date(dateString);
        if (isNaN(date.getTime())) return dateString; // Return original if invalid
        
        const month = (date.getMonth() + 1).toString().padStart(2, '0');
        const day = date.getDate().toString().padStart(2, '0');
        const year = date.getFullYear().toString().slice(-2);
        
        return `${month}/${day}/${year}`;
    }

    // Run the displayJourneyCard function when the prop journeyData.journeyID changes
    $effect(() => {
	console.log('running');
    console.log(props.journeyData.journeyID);

	if (props.journeyData.journeyID) {
		displayJourneyCard(props.journeyData.journeyID);
	}
    });

</script>

<style></style>

<!-- Updated layout with scroll snap -->
<div class="flex flex-row gap-2 w-full">
    <div class="flex items-center self-stretch">
        <button 
            class="rounded-full h-12 w-12 flex items-center justify-center bg-gray-100 hover:bg-gray-200 text-gray-800 font-semibold shadow"
            onclick={createJourneyCard}>
            <span class="text-xl">+</span>
        </button>
    </div>
    <!-- Scroll container with snap -->
    <div class="flex overflow-x-auto snap-x snap-mandatory pb-4 gap-4 w-full">
        {#each cardData as card, index}
            {#if card.cardID !== ''}
                <!-- Each card is a snap point -->
                <div class="snap-start shrink-0 w-80 relative">
                    <button 
                        type="button"
                        onclick={() => deleteJourneyCard(card.cardID, index)}
                        class="absolute -top-1 right-0 px-1.5 py-0.5 bg-red-500 hover:bg-red-600 text-white rounded-tl-md rounded-tr-lg rounded-bl-md flex items-center justify-center shadow-md z-10"
                        title="Delete card"
                    >
                        <span class="text-xs font-bold">×</span>
                    </button>
                    <form class="border border-primary-400 rounded-lg shadow-sm bg-tertiary-900 p-4 w-full">

                        <div class="mb-4">
                            <div class="flex items-center justify-between">
                                <p class="text-sm font-medium text-tertiary-500">Iteration #{card.iteration}</p>
                                <p class="text-sm font-medium text-tertiary-500">{formatDate(card.datePosted)}</p>
                            </div>
                        </div>

                        <div class="mb-3">
                            <label for={`grindSetting${index + 1}`} class="block text-sm font-medium text-tertiary-200 mb-1">Grind Setting</label>
                            <div class="relative">
                                <div class="absolute top-0 left-0 h-[1px] w-1/3 bg-primary-200"></div>
                                <input 
                                    type="text" 
                                    id={`grindSetting${index + 1}`} 
                                    bind:value={card.grindSetting} 
                                    required
                                    class="w-full p-2 border-0 rounded-md text-tertiary-500 bg-tertiary-900 focus:ring-primary-500 focus:border-primary-500" 
                                />
                            </div>
                        </div>
                        
                        <div class="mb-3">
                            <label for={`shotTime${index + 1}`} class="block text-sm font-medium text-tertiary-200 mb-1">Shot Time</label>
                            <div class="relative">
                                <div class="absolute top-0 left-0 h-[1px] w-1/3 bg-primary-200"></div>
                                <input 
                                    type="text" 
                                    id={`shotTime${index + 1}`} 
                                    bind:value={card.shotTime} 
                                    required 
                                    class="w-full p-2 border-0 rounded-md text-tertiary-500 bg-tertiary-900 focus:ring-primary-500 focus:border-primary-500"
                                />
                            </div>
                        </div>
                        
                        <div class="mb-4 relative">
                            <label for={`notes${index + 1}`} class="block text-sm font-medium text-tertiary-200 mb-1">Notes</label>
                            <div class="relative">
                                <div class="absolute top-0 left-0 h-[1px] w-1/3 bg-primary-200"></div>
                                <textarea 
                                    id={`notes${index + 1}`} 
                                    bind:value={card.notes} 
                                    required
                                    class="w-full p-2 border-0 rounded-md text-tertiary-500 bg-tertiary-900 focus:ring-primary-500 focus:border-primary-500 min-h-[80px]"
                                ></textarea>
                            </div>
                        </div>
                        
                        <button 
                            type="button" 
                            onclick={() => updateJourneyCard(index)}
                            class="w-full bg-primary-500 hover:bg-primary-600 text-white font-medium py-2 px-4 rounded-md shadow-sm">
                            Update
                        </button>
                    </form>
                </div>
            {/if}
        {/each}
    </div>
</div>
