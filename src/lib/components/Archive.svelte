<!-- base component of the archive page
 intends to show archived espresso setups 
 and allow for repeated updates to "journey cards" -->

 <script lang="ts">
    import { goto } from '$app/navigation';
    import { onMount } from 'svelte';
    import { Accordion, AccordionItem } from '@skeletonlabs/skeleton';
    import JourneyCard from './JourneyCard.svelte';

    let journeyImage1 = '/images/espresso1.jpg';
    let journeyImage2 = '/images/espresso2.jpg';
    let journeyImage3 = '/images/espresso3.jpg';
    
    let drink1 = '';
    let grinder1 = '';
    let grindSetting1 = '';
    let coffeeBeans1 = '';
    let brewingDevice1 = '';
    let iteration1 = '';
    let journey_id1 = '';
    let journey_id2 = '';
    let journey_id3 = '';

    let drink2 = '';
    let grinder2 = '';
    let grindSetting2 = '';
    let coffeeBeans2 = '';
    let brewingDevice2 = '';
    let iteration2 = '';

    let drink3 = '';
    let grinder3 = '';
    let grindSetting3 = '';
    let coffeeBeans3 = '';
    let brewingDevice3 = '';
    let iteration3 = '';

    let cardPropData1 = {};
    let cardPropData2 = {};
    let cardPropData3 = {};

    let cardProp1 = () => ({
        journeyID: journey_id1
    });

    let cardProp2 = () => ({
        journeyID: journey_id2
    });

    let cardProp3 = () => ({
        journeyID: journey_id3
    });

    // Add state to track which accordion item is open
    let openItem = -1; // -1 means all closed

    // Function to toggle accordion items
    function toggleAccordion(index) {
        openItem = openItem === index ? -1 : index;
    }

    const displayArchive = async () => {
        try {
            const response = await fetch('http://localhost:4000/archiveSetup', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            if (response.ok) {
                const data = await response.json();
                console.log('Archive:', data);
                const journeys = data.journeys;
                console.log('journeys:', journeys);
                
                if (journeys.length > 0) {
                    // Destructure the first setup object
                    drink1 = journeys[0].drink;
                    grinder1 = journeys[0].grinder;
                    grindSetting1 = journeys[0].grindSetting;
                    coffeeBeans1 = journeys[0].coffeeBeans;
                    brewingDevice1 = journeys[0].brewingDevice;
                    iteration1 = journeys[0].iteration;
                    journey_id1 = journeys[0].id;
                    cardPropData1 = cardProp1();
                }

                if (journeys.length > 1) {
                    // Destructure the second setup object
                    drink2 = journeys[1].drink;
                    grinder2 = journeys[1].grinder;
                    grindSetting2 = journeys[1].grindSetting;
                    coffeeBeans2 = journeys[1].coffeeBeans;
                    brewingDevice2 = journeys[1].brewingDevice;
                    iteration2 = journeys[1].iteration;
                    journey_id2 = journeys[1].id;
                    cardPropData2 = cardProp2();
                }

                if (journeys.length > 2) {
                    // Destructure the third setup object
                    drink3 = journeys[2].drink;
                    grinder3 = journeys[2].grinder;
                    grindSetting3 = journeys[2].grindSetting;
                    coffeeBeans3 = journeys[2].coffeeBeans;
                    brewingDevice3 = journeys[2].brewingDevice;
                    iteration3 = journeys[2].iteration;
                    journey_id3 = journeys[2].id;
                    cardPropData3 = cardProp3();
                }
            } else {
                const error = await response.json();
                console.error('Failed to fetch journeys:', error.message);
            }
        } catch (err) {
            console.error('Error fetching journeys:', err);
        }
    }

    onMount(() => {
        displayArchive();
    });
</script>

<style>

    .accordion-header {
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        border-radius: 0.375rem;
        overflow: hidden; /* Keep background inside rounded corners */
    }
    
    /* Other styles remain the same */

    
    
    /* Modified layout styles */
    .outerContainer {
        display: flex;
        flex-direction: row;
        align-items: flex-start;
        gap: 20px;
        width: 100%;
    }

    .innerContainer {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        gap: 30px;
        width: 100%;
    }

    /* Each journey container will be a column */

    /* Card will take full width of its container */
    .journeyInfoCard {
        width: 100%;
    }

    .journeyCard {
        width: 100%;
    }
</style>

<div class="outerContainer">
    <div class="innerContainer">
        <Accordion>
            <!-- First Journey -->
            <AccordionItem open={openItem === 0}>
                <svelte:fragment slot="lead">
                    <div class="flex items-center space-x-2">
                        <span class="badge bg-primary-500">1</span>
                    </div>
                </svelte:fragment>
                <svelte:fragment slot="summary">
                    <button
                        type="button"
                        class="flex items-center space-x-3 w-full text-left"
                        style="background-image: url({journeyImage1}); background-size: cover; background-position: center;"
                        on:click|stopPropagation={() => toggleAccordion(0)}
                        on:keydown={(e) => e.key === 'Enter' && toggleAccordion(0)}
                    >
                        <div class="py-2 px-3 rounded-md flex items-center space-x-3 flex-grow">
                            <p class="whitespace-nowrap">Drink: {drink1}</p>
                            <div class="h-4 border-r border-slate-300"></div>
                            <p class="whitespace-nowrap truncate">Coffee: {coffeeBeans1}</p>
                        </div>
                        <div class="h-full w-14 max-w-[56px] flex-shrink-0">
                            <!-- No image needed here since we're using background image -->
                        </div>
                    </button>
                </svelte:fragment>
                <svelte:fragment slot="content">
                    <div class="journey-content">
                        <div class="journeyInfoCard border border-slate-300 rounded-md overflow-hidden">
                            <header class="bg-blue-gray-100 p-3 border-b border-blue-gray-200 font-semibold text-center">
                                Espresso Journey 1
                            </header>
                            <div class="p-4">
                                <div class="flex items-center justify-between">
                                    <div class="flex items-center space-x-3">
                                        <p class="whitespace-nowrap">Drink: {drink1}</p>
                                        <div class="h-4 border-r border-slate-300"></div>
                                        <p class="whitespace-nowrap">Coffee Beans: {coffeeBeans1}</p>
                                        <div class="h-4 border-r border-slate-300"></div>
                                        <p class="whitespace-nowrap">Grinder: {grinder1}</p>
                                        <div class="h-4 border-r border-slate-300"></div>
                                        <p class="whitespace-nowrap">Brewing Device: {brewingDevice1}</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="journeyCard">
                            <JourneyCard journeyData={cardPropData1}/>
                        </div>
                    </div>
                </svelte:fragment>
            </AccordionItem>

            <!-- Second Journey -->
            <AccordionItem open={openItem === 1}>
                <svelte:fragment slot="lead">
                    <div class="flex items-center space-x-2">
                        <span class="badge bg-primary-500">2</span>
                    </div>
                </svelte:fragment>
                <svelte:fragment slot="summary">
                    <button
                        type="button"
                        class="flex items-center space-x-3 w-full text-left"
                        style="background-image: url({journeyImage2}); background-size: cover; background-position: center;"
                        on:click|stopPropagation={() => toggleAccordion(1)}
                        on:keydown={(e) => e.key === 'Enter' && toggleAccordion(1)}
                    >
                        <div class="py-2 px-3 rounded-md flex items-center space-x-3 flex-grow">
                            <p class="whitespace-nowrap">Drink: {drink2}</p>
                            <div class="h-4 border-r border-slate-300"></div>
                            <p class="whitespace-nowrap truncate">Coffee: {coffeeBeans2}</p>
                        </div>
                        <div class="h-full w-14 max-w-[56px] flex-shrink-0">
                            <!-- No image needed here since we're using background image -->
                        </div>
                    </button>
                </svelte:fragment>
                <svelte:fragment slot="content">
                    <div class="journey-content">
                        <div class="journeyInfoCard border border-slate-300 rounded-md overflow-hidden">
                            <header class="bg-blue-gray-100 p-3 border-b border-blue-gray-200 font-semibold text-center">
                                Espresso Journey 2
                            </header>
                            <div class="p-4">
                                <div class="flex items-center justify-between">
                                    <div class="flex items-center space-x-3">
                                        <p class="whitespace-nowrap">Drink: {drink2}</p>
                                        <div class="h-4 border-r border-slate-300"></div>
                                        <p class="whitespace-nowrap">Coffee Beans: {coffeeBeans2}</p>
                                        <div class="h-4 border-r border-slate-300"></div>
                                        <p class="whitespace-nowrap">Grinder: {grinder2}</p>
                                        <div class="h-4 border-r border-slate-300"></div>
                                        <p class="whitespace-nowrap">Brewing Device: {brewingDevice2}</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="journeyCard">
                            <JourneyCard journeyData={cardPropData2}/>
                        </div>
                    </div>
                </svelte:fragment>
            </AccordionItem>

            <!-- Third Journey -->
            <AccordionItem open={openItem === 2}>
                <svelte:fragment slot="lead">
                    <div class="flex items-center space-x-2">
                        <span class="badge bg-primary-500">3</span>
                    </div>
                </svelte:fragment>
                <svelte:fragment slot="summary">
                    <button
                        type="button"
                        class="flex items-center space-x-3 w-full text-left"
                        style="background-image: url({journeyImage3}); background-size: cover; background-position: center;"
                        on:click|stopPropagation={() => toggleAccordion(2)}
                        on:keydown={(e) => e.key === 'Enter' && toggleAccordion(2)}
                    >
                        <div class="py-2 px-3 rounded-md flex items-center space-x-3 flex-grow">
                            <p class="whitespace-nowrap">Drink: {drink3}</p>
                            <div class="h-4 border-r border-slate-300"></div>
                            <p class="whitespace-nowrap truncate">Coffee: {coffeeBeans3}</p>
                        </div>
                        <div class="h-full w-14 max-w-[56px] flex-shrink-0">
                            <!-- No image needed here since we're using background image -->
                        </div>
                    </button>
                </svelte:fragment>
                <svelte:fragment slot="content">
                    <div class="journey-content">
                        <div class="journeyInfoCard border border-slate-300 rounded-md overflow-hidden">
                            <header class="bg-blue-gray-100 p-3 border-b border-blue-gray-200 font-semibold text-center">
                                Espresso Journey 3
                            </header>
                            <div class="p-4">
                                <div class="flex items-center justify-between">
                                    <div class="flex items-center space-x-3">
                                        <p class="whitespace-nowrap">Drink: {drink3}</p>
                                        <div class="h-4 border-r border-slate-300"></div>
                                        <p class="whitespace-nowrap">Coffee Beans: {coffeeBeans3}</p>
                                        <div class="h-4 border-r border-slate-300"></div>
                                        <p class="whitespace-nowrap">Grinder: {grinder3}</p>
                                        <div class="h-4 border-r border-slate-300"></div>
                                        <p class="whitespace-nowrap">Brewing Device: {brewingDevice3}</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="journeyCard">
                            <JourneyCard journeyData={cardPropData3}/>
                        </div>
                    </div>
                </svelte:fragment>
            </AccordionItem>
        </Accordion>
    </div>
</div>
