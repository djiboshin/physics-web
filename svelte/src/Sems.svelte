<script>
import { seminars, currentWeekNum } from './stores.js';
import PhotoInput from './PhotoInput.svelte';
import { Button, ButtonGroup, ButtonToolbar} from 'sveltestrap';
import { Accordion, AccordionItem } from 'sveltestrap';
import { Form, FormGroup, FormText, Input, Label } from 'sveltestrap';
import { Card, CardBody } from 'sveltestrap';
import { Col, Container, Row, CardHeader} from 'sveltestrap';
import { Collapse} from 'sveltestrap';

let openedLists = {}
let usedFileInputs = {}

const resize = (el) => {
	el.target.style.height = 'auto'
	el.target.style.height = 4 + el.target.scrollHeight + 'px';
};

function changePosition(i, delta) {
	if (0<=(i+delta) && (i+delta)<$seminars[$currentWeekNum].length){
		[$seminars[$currentWeekNum][i], $seminars[$currentWeekNum][i+delta]] = [$seminars[$currentWeekNum][i+delta], $seminars[$currentWeekNum][i]]
	}
	
}

function deleteSeminar(index) {
	$seminars[$currentWeekNum].splice(index, 1);
    $seminars[$currentWeekNum] = $seminars[$currentWeekNum]
}

</script>
{#each $seminars[$currentWeekNum] as sem, i}
<Card>
<CardHeader style="background:{sem.date_color}; color:{sem.date_text_color}">

    <Row>
        <Col class="col-sl-5">
            {new Date(sem.datetime).toLocaleDateString('en-US',{month: 'long', day: 'numeric', weekday: 'long'})}
            <br>
            {new Date(sem.datetime).toLocaleTimeString('ru-RU',{hour: '2-digit', minute: '2-digit'})}, {sem.type}
        </Col>
        <Col class="col-sl-5">
        <ButtonGroup>
        <Button
            color={openedLists[$currentWeekNum + '_' + i]?'warning':"primary"}
            class="mb-1"
            on:click={() => openedLists[$currentWeekNum + '_' + i] = !openedLists[$currentWeekNum + '_' + i]}>
            {openedLists[$currentWeekNum + '_' + i]?'Close':'Edit'}
        </Button>
            <Button class="mb-1" on:click={() => changePosition(i, -1)}>up</Button>
            <Button class="mb-1" on:click={() => changePosition(i, 1)}>down</Button>
        <Button class="mb-1" color="danger" on:click={() => (deleteSeminar(i))}>delete</Button>
        </ButtonGroup>
        </Col>
    </Row>
</CardHeader>
<Collapse isOpen={openedLists[$currentWeekNum + '_' + i]}>
<CardBody>
        <div class="sem">
            <Form>
                <FormGroup>
                    <Label>Speaker</Label>
                    <Input rows={1} type="textarea" on:input={resize} on:focus={resize} bind:value={sem.speaker_name}/>
                </FormGroup>
                <FormGroup>
                    <Label>Name</Label>
                    <Input type="textarea" on:input={resize} on:focus={resize} bind:value={sem.name}
                    style="background-color:{sem.background_color}; color:{sem.text_color}"/>
                </FormGroup>
                <Container>
                    <Row class="align-self-center">
                        <Col class="col-3">
                            <FormGroup>
                                <Label>Date</Label>
                                <Input type="color" bind:value={sem.date_color}/>
                            </FormGroup>
                        </Col>
                        <Col class="col-3">
                            <FormGroup>
                                <Label>Date text</Label>
                                <Input type="color" bind:value={sem.date_text_color}/>
                            </FormGroup>
                        </Col>
                        <Col class="col-3">
                            <FormGroup>
                                <Label>Background</Label>
                                <Input type="color" bind:value={sem.background_color}/>
                            </FormGroup>
                        </Col>
                        <Col class="col-3">
                            <FormGroup>
                                <Label>Text</Label>
                                <Input type="color" bind:value={sem.text_color}/>
                            </FormGroup>
                        </Col>
                        
                    </Row>
                </Container>
                    <PhotoInput sem={sem} usedFileInputs={usedFileInputs} id={$currentWeekNum + '_' + i}>
                </PhotoInput>
                <FormGroup>
                    <Input type="checkbox" label="Friday?" bind:checked={sem.is_special}/>
                </FormGroup>
            </Form>
        </div>
</CardBody>
</Collapse>
</Card>
{/each}