<script>
	import { Form, Input, FormGroup, Button } from '@sveltestrap/sveltestrap';
    import * as api from "../lib/services/api.js";
	import { navigate, link } from "svelte-routing";
  
	let viewmodel = $state({ username : "", password : ""});
	let errorMessage = $state("");
	let validated = $state(false);

	const handleSubmit = async() => {
		// Reset error message
		errorMessage = "";

		var response = await api.signin(
            viewmodel.username, 
            viewmodel.password
        );

		if (response.ok) {
			// Redirect to the expenses page
			navigate("/expenses");
		} else {
			// Show an error message
			errorMessage = response.data.message;
			validated = false;
		}
	}
</script>

<section style="width: 400px; margin: 100px auto; height: 500px;">
	<h1 class="mb-4">Sign in</h1>

	<div class="alert alert-secondary" role="alert">
		<div>For testing, you can use the following credentials:</div>
		<br>
		<div><b>Username:</b> jane <b>Password:</b> pass</div>
		<div><b>Username:</b> john <b>Password:</b> pass</div>
	</div>

	{#if errorMessage}
		<div class="alert alert-danger" role="alert">
			{errorMessage}
		</div>
	{/if}

	<Form {validated} onsubmit={(e) => { e.preventDefault(); handleSubmit(); }}>
		<FormGroup floating label="Username">
			<Input bind:value={viewmodel.username} placeholder="Enter a value" required feedback="The username is required" />
		</FormGroup>
		<FormGroup floating label="Password">
			<Input bind:value={viewmodel.password} placeholder="Enter a value" type="password" required feedback="The password is required" />
		</FormGroup>

		<div class="d-flex justify-content-end">
			<Button type="submit" onclick={() => (validated = true)} class="w-100">Sign in</Button>
		</div>

		<div class="d-flex justify-content-center pt-4">
			<span>Dont have an account? Cliek here to <a href="/signup" use:link>sign up</a></span>
		</div>
	</Form>
	
</section>