<svelte:head>
	<title>Семинары</title>
</svelte:head>

<script>
import { onMount } from "svelte";

let isLoading = false;
let preview;
let socket;

let file_input;
let url_input;
let img_prev;

let week_forward = 1;
let friday_text = "";
let friday_photo_url = null;
let friday_photo_file = null;

$: params = {week_forward: week_forward,
	type: 'png',
	extra_seminar: {
		name: friday_text.toString().trim()==''?null:friday_text,
		background_color: "#022950",
		photo_src: friday_photo_file?friday_photo_file:friday_photo_url,
		text_color: 'white',
	}
};

function UpdatePreview(params) {
	console.log(params);
	isLoading = true;
	socket.send(JSON.stringify(params));
}

function UpdateFile() {
	if (file_input.files.length>0) {
		PhotoToBase64(file_input.files[0]);
		img_prev.hidden = false
		img_prev.src = URL.createObjectURL(file_input.files[0])
	} else {
		PhotoToBase64(null);
		img_prev.hidden = true
	}
}

function UpdateURL(e) {
	friday_photo_url = url_input.value
}

function PhotoToBase64(file) {
	if (!file) {
		friday_photo_file = null
	} else {
		let reader = new FileReader();
		reader.onloadend = () => {friday_photo_file = reader.result};
		reader.onerror = () => {console.log(reader.error)};
		reader.readAsDataURL(file);
	};
}

let a;
async function Base64toBlob(b) {
	return fetch(b).then(r => {return r.blob()})
}

onMount (async () => {
	socket = new WebSocket("ws://" + document.location.host + document.location.pathname + "ws/render_b64");
	socket.onopen = function(event) {
		UpdatePreview(params);
	};
	socket.onmessage = async function(event) {
		preview.blob = await Base64toBlob(event.data)
		preview.src = URL.createObjectURL(preview.blob);
		isLoading = false;
	};
	url_input.addEventListener('paste', (event) => {
		let items = event.clipboardData.items;
		for (var i = 0; i < items.length; i++) {
			if (items[i].type.indexOf("image") == -1) continue;
			event.preventDefault();
			var blob = items[i].getAsFile();
			let container = new DataTransfer();
			container.items.add(blob);
			file_input.files = container.files;			
			UpdateFile();
			break
		}
		
});
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
        <img bind:this={preview} on:load={() => URL.revokeObjectURL(preview.src)} alt="{isLoading?'Loading...':'ERROR'}" class="preview" style="opacity: {isLoading?0.2:1}">
    </div>
    <div class="panel">
        <div class="week">
            <label for="week_forward"><h3>week_forward</h3></label>
            <input type="number" name="week_forward" min="-10" max="10" bind:value={week_forward}>
        </div>
        <div class="text">
            <label for="fr_name"><h3>Текст</h3></label>
            <textarea name="fr_name" bind:value={friday_text}></textarea>
        </div>
        <div class="photo">
			<h3>Фото</h3>

			<label for="fr_photo_url">URL или вставить фото</label>
			<input type="url" name="fr_photo_url" class="url_input" bind:this={url_input} on:change={UpdateURL}>

            <label for="fr_photo_url">Файл</label>
			<input class="file_input" type="file" accept="image/*" name="fr_photo_file" bind:this={file_input} on:change={UpdateFile}>
			<img class="img_prev" alt="файл" bind:this={img_prev} hidden>
            <button class="delete" on:click={() => {file_input.value = ""; UpdateFile()}}>Удалить файл</button>
        </div>
        <button class="submit" disabled={isLoading} on:click={() => UpdatePreview(params)}>Сабмит</button>
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
	.preview {
		min-width: 660px;
	}
    .panel {
        min-width: 300px;
		max-width: 630px;
        padding: 10px;
    }
	img {
		margin: auto;
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
	.url_input {
		width: 100%;
	}
	.url_input:invalid {
		background-color: red;
	}
	.url_input:valid {
		background-color: white;
	}
	.img_prev{
		height: 50px;
	}
    .photo {
        margin-bottom: 10px;
    }
	.delete {
		background-color: #E84D3C;
		color:black;
	}
	.submit {
		background-color: #2FCE73;
		color:black;
	}
	.submit:disabled {
		background-color: #E84D3C;
		color:black;
	}
	.copy {
		color:black;
	}
</style>
