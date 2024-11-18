const BACKEND_API_URL = 'http://localhost:5000/api';

export const signin = async (username, password) => {
    const resposne = await sendHttpRequest(`${BACKEND_API_URL}/signin`, "POST", { username, password });
    return resposne;
}

export const signout = async () => {
    const resposne = await sendHttpRequest(`${BACKEND_API_URL}/signout`, "GET");
    return resposne;
}

export const signup = async (firstname, lastname, username, password) => {
    const resposne = await sendHttpRequest(`${BACKEND_API_URL}/signup`, "POST", { firstname, lastname, username, password });
    return resposne;
}

export const getUserInfo = async () => {
    const resposne = await sendHttpRequest(`${BACKEND_API_URL}/user-info`, "GET");
    return resposne;
}

export const getUserExpenses = async () => {
    const resposne = await sendHttpRequest(`${BACKEND_API_URL}/expenses`, "GET");
    return resposne;
}

export const getUserExpense = async (id) => {
    const resposne = await sendHttpRequest(`${BACKEND_API_URL}/expenses/${id}`, "GET");
    return resposne;
}

export const createUserExpense = async (description, amount, date, category) => {
    const resposne = await sendHttpRequest(`${BACKEND_API_URL}/expenses`, "POST", { description, amount, date, category });
    return resposne;
};

export const updateUserExpense = async (id, description, amount, date, category) => {
    const resposne = await sendHttpRequest(`${BACKEND_API_URL}/expenses/${id}`, "PUT", { description, amount, date, category });
    return resposne;
};

export const deleteUserExpense = async (id) => {
    const resposne = await sendHttpRequest(`${BACKEND_API_URL}/expenses/${id}`, "DELETE");
    return resposne;
};

// Auxiliary function to send HTTP requests
const sendHttpRequest = async (endpoint, method, body) => {
    const response = await fetch(endpoint, {
        method: method,
        headers: {
            "Content-Type": "application/json"
        },
        credentials: "include",
        body: body ? JSON.stringify(body) : null,
    });

    return {
        ok: response.ok,
        data: await response.json()
    };
};
