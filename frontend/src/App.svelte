<script>
  import { onMount } from "svelte";
  import * as api from "./lib/services/api.js";
  import { Router, Route, navigate } from "svelte-routing";
  import Expenses from "./pages/Expenses.svelte";
  import Signin from "./pages/Signin.svelte";
  import Signup from "./pages/Signup.svelte";
  import Signout from "./pages/Signout.svelte";
  import Home from "./pages/Home.svelte";

  onMount(async () => {
    const response = await api.getUserInfo();
    if (response.ok && response.data) {
      navigate("/expenses");
    } else {
      navigate("/signin");
    }
  });
</script>

<div class="app">
  <main class="container">
    <Router>
      <Route path="/signin"><Signin /></Route>
      <Route path="/signup"><Signup /></Route>
      <Route path="/signout"><Signout /></Route>
      <Route path="/expenses"><Expenses /></Route>
      <Route path="/"><Home /></Route>
    </Router>
  </main>
</div>
