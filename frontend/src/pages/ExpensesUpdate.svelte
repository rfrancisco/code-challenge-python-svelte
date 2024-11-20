<script>
  import { Button, Form, FormGroup, Input, Modal, ModalBody, ModalFooter } from "@sveltestrap/sveltestrap";
  import * as api from "../lib/services/api.js";
  import { onMount } from "svelte"; 

  let {id, close} = $props();
  let open = $state(true);
  let viewmodel = $state({ id: 0, description: '', amount: 0, category: '', date: new Date().toISOString().split('T')[0]});
  let errorMessage = $state("");
  let validated = $state(false);

  // Initialize the component
  onMount(async () => {
    const response = await api.getUserExpense(id);
    const expense = response.data;
    viewmodel = {
      id: expense.id,
      description: expense.description,
      amount: expense.amount,
      category: expense.category,
      date: expense.date
    }
  });

    // Hide the modal when the user clicks the cancel or close button and notify parent component
  const cancelModal = () => {
    open = false;
    // Notify the parent component passing 'false' indicating that an expense was not updated
    close(false);
  };

  // Update the expense and notify the parent component
  const handleSubmit = async () => {
    // Reset error message
    errorMessage = '';

    var response = await api.updateUserExpense(id, viewmodel.description, viewmodel.amount, viewmodel.date, viewmodel.category);

    if (response.ok) {
      // Hide the modal and notify parent component
      open = false;
      // Notify the parent component passing 'false' indicating that an expense was updated
      close(true);
    } else {
      // Show an error message
      errorMessage = response.data.message;
      validated = false;
    }
  }
</script>

<Modal isOpen={open} toggle={cancelModal}>
  <Form {validated} onsubmit={(e) => { e.preventDefault(); handleSubmit(); }}>
    <ModalBody>
      <h1 class="mb-4 mt-2 fs-3">Update expense</h1>
      
      {#if errorMessage}
        <div class="alert alert-danger" role="alert">
          {errorMessage}
        </div>
      {/if}

      <FormGroup floating label="Date">
        <Input bind:value={viewmodel.date} placeholder="Enter a value" type="date" required feedback="The date is required" />
      </FormGroup>
      <FormGroup floating label="Category">
        <Input bind:value={viewmodel.category} placeholder="Enter a value" required feedback="The category is required" />
      </FormGroup>
      <FormGroup floating label="Amount">
        <Input bind:value={viewmodel.amount} placeholder="Enter a value" type="number" required feedback="The amount is required" />
      </FormGroup>
      <FormGroup floating label="Description">
        <Input bind:value={viewmodel.description} placeholder="Enter a value" required feedback="The description is required" />
      </FormGroup>
    </ModalBody>

    <ModalFooter>
      <Button color="primary" type="submit" onclick={() => (validated = true)}>Save</Button>
      <Button color="secondary" type="button" onclick={cancelModal}>Cancel</Button>
    </ModalFooter>
  </Form>
</Modal>
