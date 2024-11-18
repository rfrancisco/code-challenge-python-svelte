<script>
	import { Table, Button } from "@sveltestrap/sveltestrap";
    import { onMount } from "svelte";
    import * as api from "../lib/services/api.js";
    import { navigate } from "svelte-routing";
    import ExpensesCreate from "./ExpensesCreate.svelte";
    import ExpensesUpdate from "./ExpensesUpdate.svelte";

	let expenses = $state(null);
	let createModalOpen = $state(false);
	let updateModalOpen = $state(false);
	let selectedId = $state(0);

	// Initialize the component
	onMount(async () => {
		const response = await api.getUserInfo();
		const isAuthenticated = response.ok && response.data;

      	if (isAuthenticated) {
			loadExpenses();
		} else {
        	navigate("/signin");
      	}
	});

	const loadExpenses = async () => {
		const response = await api.getUserExpenses();
		expenses = response.data;
	};

    const createExpense = () => {
		createModalOpen = false;
		setTimeout(() => {
			createModalOpen = true;
		}, 1);
    };

    const updateExpense = (id) => {
		selectedId = id;
		updateModalOpen = false;
		setTimeout(() => {
			updateModalOpen = true;
		}, 1);
    };

	const deleteExpense = async (id) => {
        await api.deleteUserExpense(id);
        expenses = expenses.filter((expense) => expense.id !== id);
	};
</script>

<div class="mb-4">
	<h1>My expenses</h1>
</div>

<div class="mb-4 d-flex justify-content-between">
	<Button color="primary" onclick={() => createExpense()}>Create</Button>
	<Button color="danger" onclick={() => navigate("/signout")}>Sign out</Button>
</div>

<section class="w-100">
	<Table hover class="w-100 align-middle">
		<colgroup>
			<col style="width: 50px" />
			<col style="width: 140px" />
			<col style="width: 180px" />
			<col style="width: 80px" />
			<col />
			<col style="width: 180px" />
		</colgroup>
		<thead>
			<tr>
				<th>#</th>
				<th>Date</th>
				<th>Category</th>
				<th class="text-end">Amount</th>
				<th>Description</th>
				<th></th>
			</tr>
		</thead>
		<tbody>
			{#each expenses as expense}
				<tr onclick={() => updateExpense(expense.id)} style="cursor:pointer">
					<th scope="row">{expense.id}</th>
					<td>{expense.date}</td>
					<td>{expense.category}</td>
					<td class="text-end">{expense.amount} €</td>
					<td>{expense.description}</td>
					<td class="text-end">
						<Button color="primary" outline onclick={(e) => {e.stopPropagation(); updateExpense(expense.id)}}>Edit</Button>
						<Button color="danger" outline onclick={(e) => {e.stopPropagation(); deleteExpense(expense.id)}}>Delete</Button>
					</td>
				</tr>
			{/each}
		</tbody>
	</Table>
</section>

{#if createModalOpen}
	<ExpensesCreate close={created => {
		if (created) {
			loadExpenses();
		}
	}} />
{/if}


{#if updateModalOpen}
	<ExpensesUpdate id={selectedId} close={updated => {
		if (updated) {
			loadExpenses();
		}
	}} />
{/if}
