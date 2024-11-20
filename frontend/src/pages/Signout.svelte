<script>
  import { onMount } from "svelte";
  import * as api from "../lib/services/api.js";
  import { navigate } from "svelte-routing";

  onMount(async () => {
    // Sign out the user
    await api.signout();
    // Redirect to the sign in page
    navigate("/signin");
  });
</script>
