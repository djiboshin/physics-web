
<script>
import { onMount } from "svelte";
import { seminars, currentWeekNum } from './stores.js';
import { Form, FormGroup, FormText, Input, Label } from 'sveltestrap';
import { Button, ButtonGroup, ButtonToolbar} from 'sveltestrap';
import { Col, Container, Row, CardHeader} from 'sveltestrap';
import { Image } from 'sveltestrap';

export let sem;
export let usedFileInputs;
export let id;

let url_input;
let file_input;
let img_prev;

function UpdateURL (event) {
    event.preventDefault();
    sem.photo_src = event.target.value
    usedFileInputs[id] = false
}


function ClearURL (event) {
    event.preventDefault();
    sem.photo_src = null
    usedFileInputs[id] = false
}

function PhotoToBase64(file) {
    let reader = new FileReader();
    reader.onloadend = () => {
        sem.photo_src = reader.result;
        $seminars[$currentWeekNum] = $seminars[$currentWeekNum]
        usedFileInputs[id] = true
    };
    reader.onerror = () => {console.log(reader.error)};
    reader.readAsDataURL(file);
}

function addHandlerURL(event) {
    event.target.addEventListener('paste', (event) => {
		let items = event.clipboardData.items;
		for (var i = 0; i < items.length; i++) {
			if (items[i].type.indexOf("image") == -1) continue;
            event.preventDefault();
			let blob = items[i].getAsFile();
			let container = new DataTransfer();
			container.items.add(blob);
            PhotoToBase64(container.files[0])
            event.currentTarget.nextElementSibling.nextElementSibling.src = sem.photo_src
			break
		}
	})
}
onMount (async () => {
    
})

</script>

<FormGroup>
    <Label>Photo</Label>
    <Input rows=1 srtle="resize: none;" wrap="off" value={usedFileInputs[id]?'':sem.photo_src} on:change={UpdateURL} on:focus|once={addHandlerURL}/><br>
    <Image  thumbnail style="max-height:100px" alt="" src={usedFileInputs[id]?sem.photo_src:""}/>
    <Button color="danger" size="sm" on:click={ClearURL}>Delete Photo</Button>
</FormGroup>
