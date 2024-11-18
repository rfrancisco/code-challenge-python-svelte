<script>
    import { Form, Input, FormGroup, Button, Row, Col, } from "@sveltestrap/sveltestrap";
    import * as api from "../lib/services/api.js";
    import { navigate, link } from "svelte-routing";

    let viewmodel = $state({ firstname: "", lastname: "", username: "", password: "" });
    let errorMessage = $state("");
    let validated = $state(false);

    const handleSubmit = async () => {
        // Reset error message
        errorMessage = "";

        var response = await api.signup(
            viewmodel.firstname,
            viewmodel.lastname,
            viewmodel.username,
            viewmodel.password,
        );

        if (response.ok) {
            // Redirect to the sign in page
            navigate("/signin");
        } else {
            // Show an error message
            errorMessage = response.data.message;
            validated = false;
        }
    };
</script>

<section style="width: 400px; margin: 100px auto; height: 500px;">
    <h1 class="mb-4">Sign up</h1>

    {#if errorMessage}
        <div class="alert alert-danger" role="alert">
            {errorMessage}
        </div>
    {/if}

    <Form {validated} onsubmit={(e) => { e.preventDefault(); handleSubmit(); }}>
        <Row>
            <Col>
                <FormGroup floating label="First Name">
                    <Input bind:value={viewmodel.firstname} placeholder="Enter a value" required feedback="The first name is required" />
                </FormGroup>
            </Col>
            <Col>
                <FormGroup floating label="Last Name">
                    <Input bind:value={viewmodel.lastname} placeholder="Enter a value" required feedback="The last name is required" />
                </FormGroup>
            </Col>
        </Row>
        <FormGroup floating label="Username">
            <Input bind:value={viewmodel.username} placeholder="Enter a value" required feedback="The username is required" />
        </FormGroup>
        <FormGroup floating label="Password">
            <Input bind:value={viewmodel.password} placeholder="Enter a value" type="password" required feedback="The password is required" />
        </FormGroup>

        <div class="d-flex justify-content-end">
            <Button type="submit" onclick={() => (validated = true)} class="w-100">Sign up</Button>
        </div>

        <div class="d-flex justify-content-center pt-4">
            <span>Already have an account? Click here to <a href="/signin" use:link>sign in</a></span>
        </div>
    </Form>
</section>
