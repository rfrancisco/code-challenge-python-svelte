<script>
    import { onMount } from "svelte";
    import * as api from "../lib/services/api.js";
    import { navigate } from "svelte-routing";

    onMount(async () => {
        const response = await api.getUserInfo();
        const isAuthenticated = response.ok && response.data;

        if (isAuthenticated) {
            navigate("/expenses");
        } else {
            navigate("/signin");
        }
    });
</script>
