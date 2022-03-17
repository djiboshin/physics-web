<svelte:head>
	<title>Семинары</title>
</svelte:head>

<script>
import { onMount } from "svelte";
    
    let preview;
    let socket;
    let week_forward = 1;
    let file_input = null;
    let friday_text = "";
    let friday_photo = null;

    $: params = {week_forward: week_forward,
        type: 'png',
        extra_seminar: {
            name: friday_text.toString().trim()==''?null:friday_text,
            background_color: "#022950",
            photo_src: friday_photo,
            text_color: 'white',
        }
    };


    function UpdatePreview(params) {
        console.log(params);
        socket.send(JSON.stringify(params));
    }

    function UpdateClick() {
        console.log('update click');
        UpdatePreview(params)
    }

    function UpdateFile() {
        console.log('update file');
        if (file_input.files) {
            PhotoToBase64(file_input.files.length>0?file_input.files[0]:null)
        }
    }

    function PhotoToBase64(file) {
        if (!file) {
            friday_photo = null
        } else {
            let reader = new FileReader();
            reader.onloadend = () => {friday_photo = reader.result};
            reader.onerror = () => {console.log(reader.error)};
            reader.readAsDataURL(file);
        };
    }

	let a;
	async function Base64toBlob(b) {
		return fetch(b).then(r => {return r.blob()})
	}

    onMount (async () => {
        socket = new WebSocket("ws://" + document.location.host + "/ws/render_b64");
        socket.onopen = function(event) {
            UpdatePreview(params);
        };
        socket.onmessage = async function(event) {
			preview.blob = await Base64toBlob(event.data)
            preview.src = URL.createObjectURL(preview.blob);
        };
    })
    
	async function Copy () {
		navigator.clipboard.write(
			[new ClipboardItem({
				'image/png': preview.blob
			})]);
	}
    
</script>
<div class="main">
    <div class="preview">
        <img bind:this={preview} on:load={() => URL.revokeObjectURL(preview.src)} alt="Loading..." class="preview">
    </div>
    <div class="panel">
        <div class="week">
            <label for="week_forward">week_forward</label><br>
            <input type="number" name="week_forward" min="-10" max="10" bind:value={week_forward}>
        </div>
        <div class="text">
            <label for="fr_name">Текст</label><br>
            <textarea name="fr_name" bind:value={friday_text}></textarea>
        </div>
        <div class="photo">
            <label for="fr_photo">Фото</label><br>
            <input class="file_input" type="file" accept="image/*" name="fr_photo" bind:this={file_input} on:change={UpdateFile}>
            <button class="delete" on:click={() => {file_input.value = ""; UpdateFile()}}>Удалить фото</button>
        </div>
        <button class="submit" on:click={UpdateClick}>Сабмит</button>
		<button class="copy" on:click={Copy}>Скопировать png</button>
    </div>
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
    .panel {
        min-width: 300px;
		max-width: 630px;
        padding: 10px;
    }
    .week {
        margin-bottom: 10px;
    }
    .text {
        margin-bottom: 10px;
    }
    textarea {
        width: 100%;
        min-height: 200px;
    }
	.file_input {
		width: 100%;
	}
    .photo {
        margin-bottom: 10px;
    }
	.delete {
		background-color: rgb(233, 8, 8);
	}
	.submit {
		background-color: rgb(8, 161, 41);
	}
</style>
