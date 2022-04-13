<svelte:head>
	<title>Семинары</title>
</svelte:head>
<script>
import { Styles } from 'sveltestrap';
import Sems from './Sems.svelte';
import { Button, ButtonGroup, ButtonToolbar} from 'sveltestrap';
import { Accordion, AccordionItem } from 'sveltestrap';
import { Form, FormGroup, FormText, Input, Label } from 'sveltestrap';
import { Card, CardBody } from 'sveltestrap';
import { Col, Container, Row, CardHeader} from 'sveltestrap';
import { Collapse} from 'sveltestrap';


import { onMount } from "svelte";
import { seminars, currentWeekNum} from './stores.js';


let nowDate = Date.now()
$: isLoading = true;
let preview;

async function getSeminars() {
	return fetch(document.location.pathname + "seminars").then(r => r.json())
}

function addSeminar(seminar, week_forward) {
	if ($seminars.hasOwnProperty(week_forward)) {
		$seminars[week_forward] = [...$seminars[week_forward], seminar]
	} else {
		$seminars[week_forward] = [seminar]
	}
}

async function clearWeek(weekNum) {
	$seminars[weekNum] = []
}

async function reloadWeek(weekNum) {
	await clearWeek(weekNum)
	let res = await getSeminars()
	res.forEach(seminar => {
		let currentWeek = Math.floor((nowDate / (7*24*3600*1000) + 3/7))
		let seminarWeek = Math.floor((new Date(seminar.datetime)) / (7*24*3600*1000) + 3/7)
		let week_forward = seminarWeek - currentWeek
		if (week_forward == weekNum) {
			addSeminar(seminar, week_forward)
		}
	});

}

function previewReload() {
	let socket;
	socket = new WebSocket("ws://" + document.location.host + document.location.pathname + "ws/render_b64");
	socket.onopen = function(event) {
		isLoading = true
		let data = {type: 'png', seminars: $seminars[$currentWeekNum]}
		console.log(data);
		socket.send(JSON.stringify(data));
	};
	socket.onmessage = async function(event) {
		preview.blob = await fetch(event.data).then(r => {return r.blob()})
		preview.src = URL.createObjectURL(preview.blob);
		socket.close()
		isLoading = false
	};
	
}

onMount (async () => {
	let res = await getSeminars()
	res.forEach(seminar => {
		let currentWeek = Math.floor((nowDate / (7*24*3600*1000) + 3/7))
		let seminarWeek = Math.floor((new Date(seminar.datetime)) / (7*24*3600*1000) + 3/7)
		let week_forward = seminarWeek - currentWeek
		addSeminar(seminar, week_forward)
	});
	previewReload()
});

function prevWeek() {
	if ($seminars.hasOwnProperty($currentWeekNum-1)) {
		$currentWeekNum -= 1
	} else {
		$seminars[$currentWeekNum-1] = []
		$currentWeekNum -= 1
	}
}

function nextWeek() {
	if ($seminars.hasOwnProperty($currentWeekNum+1)) {
		$currentWeekNum += 1
	} else {
		$seminars[$currentWeekNum+1] = []
		$currentWeekNum += 1
	}
}

function createSeminar() {
	let empty_seminar = {
		name: null,
		university: null,
    	speaker_name: null,
    	type: null,
    	datetime: null,
    	photo_src: null,
    	date_color: "#022950",
		date_text_color: "#FFFFFF",
    	background_color: "#022950",
    	text_color: "#FFFFFF",
		is_special: true
	}
	addSeminar(empty_seminar, $currentWeekNum)
}


</script>
<div class="main">
<Container xxl>
<Row>
<Col class="col-lg-6" style="width:660px">
	<Container md >
	<div>
		<img bind:this={preview} on:load={() => URL.revokeObjectURL(preview.src)} alt="{isLoading?'Loading...':'ERROR'}" class="preview" style="opacity: {isLoading?0.2:1}">
	</div>
	</Container>
</Col>
<Col class="col-lg-6">
	<Container lg style="max-width:660px">
		<Container fluid class="mb-2">
			<Row class="align-items-center">
				<Col align="center">
					<Button outline secondary size="md" class="w-75" on:click={prevWeek}>-1</Button>
				</Col>
				<Col align="center" class="col-5">
					WEEK_FORWARD = {$currentWeekNum}
				</Col>
				<Col align="center">
					<Button outline secondary size="md" class="w-75" on:click={nextWeek}>+1</Button>
				</Col>
			</Row>
			<Row>
				<Col align="center">
					<Button size="md" color="danger" on:click="{() => reloadWeek($currentWeekNum)}">reset week</Button>
				</Col>
			</Row>
		</Container>
			

			<Sems></Sems>
			<Container fluid class="mt-2">
				<Row>
					<Col align="center">
						<Button size="lg" color="success" on:click={createSeminar}>+</Button>
					</Col>
				</Row>
			</Container>
			<Container fluid class="mt-2">
				<Row>
					<Col align="center">
						<Button size="lg" color="info" on:click={previewReload}>Сабмит</Button>
					</Col>
				</Row>
			</Container>
	</Container>
</Col>
</Row>
</Container>
</div>

<style>
    .main {
        display: flex;
        flex-direction: row;
        flex-wrap: wrap;
        align-content: flex-start;
        justify-content: center;
        align-items: flex-start;
		position: relative;
		margin: auto;
		width: 100%;
		height: 100%;
		font-family: Muller, "Open Sans", "Helvetica Neue", Helvetica, Arial, sans-serif;
	}
	.preview {
		width: 660px;
	}
    .panel {
        padding: 10px;

    }
	img {
		margin: auto;
	}
	.sem {
		width: 100%;
		margin-bottom:20px
	}
</style>
