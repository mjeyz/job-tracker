  // ---------- MOCK AUTH SYSTEM (localStorage) ----------
    const USERS_KEY = "jobtracker_users";
    const CURRENT_USER_KEY = "jobtracker_current_user";

    // Helper: show floating toast
    function showToast(message, isError = false) {
        const toastEl = document.getElementById("liveToastMsg");
        const toastText = document.getElementById("toastText");
        toastText.innerText = message;
        toastEl.style.backgroundColor = isError ? "#b91c1c" : "#0f3b2c";
        toastEl.style.opacity = "1";
        setTimeout(() => {
            toastEl.style.opacity = "0";
        }, 2800);
    }

    // load users from localStorage or init default
    function loadUsers() {
        let users = localStorage.getItem(USERS_KEY);
        if (!users) {
            const defaultUser = {
                name: "Demo User",
                email: "demo@jobtrack.com",
                password: "demo123"
            };
            localStorage.setItem(USERS_KEY, JSON.stringify([defaultUser]));
            return [defaultUser];
        }
        return JSON.parse(users);
    }

    function saveUsers(users) {
        localStorage.setItem(USERS_KEY, JSON.stringify(users));
    }

    function getCurrentUser() {
        const userRaw = localStorage.getItem(CURRENT_USER_KEY);
        if (userRaw) return JSON.parse(userRaw);
        return null;
    }

    function setCurrentUser(user) {
        if (user) {
            localStorage.setItem(CURRENT_USER_KEY, JSON.stringify(user));
        } else {
            localStorage.removeItem(CURRENT_USER_KEY);
        }
        updateUIBasedOnAuth();
    }

    // Update navbar and dashboard sections
    function updateUIBasedOnAuth() {
        const currentUser = getCurrentUser();
        const registerNav = document.getElementById("registerNavItem");
        const loginNav = document.getElementById("loginNavItem");
        const logoutNav = document.getElementById("logoutNavItem");
        const userWelcomeSpan = document.getElementById("userWelcomeNav");
        const navUsernameSpan = document.getElementById("navUsername");
        const dashboardSection = document.getElementById("dashboardPreviewSection");
        const ctaSection = document.getElementById("ctaAnonSection");
        const dashboardUserNameSpan = document.getElementById("dashboardUserName");

        if (currentUser) {
            // logged in state
            registerNav.classList.add("d-none");
            loginNav.classList.add("d-none");
            logoutNav.classList.remove("d-none");
            userWelcomeSpan.classList.remove("d-none");
            if (navUsernameSpan) navUsernameSpan.innerText = currentUser.name.split(' ')[0] || currentUser.name;
            if (dashboardSection) {
                dashboardSection.classList.remove("d-none");
                if (dashboardUserNameSpan) dashboardUserNameSpan.innerText = currentUser.name.split(' ')[0] || currentUser.name;
                // mock dynamic app count (just for demo)
                const mockCountSpan = document.getElementById("mockAppCount");
                if (mockCountSpan) mockCountSpan.innerText = Math.floor(Math.random() * 5) + 2;
            }
            if (ctaSection) ctaSection.classList.add("d-none");
        } else {
            registerNav.classList.remove("d-none");
            loginNav.classList.remove("d-none");
            logoutNav.classList.add("d-none");
            userWelcomeSpan.classList.add("d-none");
            if (dashboardSection) dashboardSection.classList.add("d-none");
            if (ctaSection) ctaSection.classList.remove("d-none");
        }
    }

    // Register new user
    function registerUser(name, email, password) {
        let users = loadUsers();
        const existing = users.find(u => u.email === email);
        if (existing) {
            showToast("Email already registered. Try login instead.", true);
            return false;
        }
        const newUser = {name: name.trim(), email: email.trim().toLowerCase(), password: password};
        users.push(newUser);
        saveUsers(users);
        // auto login after register
        setCurrentUser({name: newUser.name, email: newUser.email});
        showToast(`Welcome ${newUser.name}! Your account is ready 🎉`);
        return true;
    }

    // Login user
    function loginUser(email, password) {
        const users = loadUsers();
        const matchedUser = users.find(u => u.email === email.toLowerCase() && u.password === password);
        if (matchedUser) {
            setCurrentUser({name: matchedUser.name, email: matchedUser.email});
            showToast(`Logged in as ${matchedUser.name}. Start tracking!`);
            return true;
        } else {
            showToast("Invalid email or password. Try demo@jobtrack.com / demo123", true);
            return false;
        }
    }

    function logoutUser() {
        setCurrentUser(null);
        showToast("You've been logged out.");
    }

    // Event Listeners & form handlers
    document.addEventListener("DOMContentLoaded", () => {
        updateUIBasedOnAuth();

        // Register form handler
        const registerForm = document.getElementById("registerForm");
        if (registerForm) {
            registerForm.addEventListener("submit", (e) => {
                e.preventDefault();
                const name = document.getElementById("regName").value.trim();
                const email = document.getElementById("regEmail").value.trim();
                const pwd = document.getElementById("regPassword").value;
                const confirm = document.getElementById("regConfirmPassword").value;
                let isValid = true;
                document.getElementById("regEmailError").innerText = "";
                document.getElementById("regPassError").innerText = "";

                if (!name || !email || !pwd) {
                    showToast("All fields are required.", true);
                    return;
                }
                if (!email.includes("@")) {
                    document.getElementById("regEmailError").innerText = "Enter valid email";
                    return;
                }
                if (pwd.length < 4) {
                    document.getElementById("regPassError").innerText = "Password must be at least 4 characters";
                    return;
                }
                if (pwd !== confirm) {
                    document.getElementById("regPassError").innerText = "Passwords do not match";
                    return;
                }
                if (registerUser(name, email, pwd)) {
                    // close modal
                    const modal = bootstrap.Modal.getInstance(document.getElementById("registerModal"));
                    if (modal) modal.hide();
                    registerForm.reset();
                }
            });
        }

        // Login form handler
        const loginForm = document.getElementById("loginForm");
        if (loginForm) {
            loginForm.addEventListener("submit", (e) => {
                e.preventDefault();
                const email = document.getElementById("loginEmail").value.trim();
                const pwd = document.getElementById("loginPassword").value;
                const errorDiv = document.getElementById("loginErrorMsg");
                if (!email || !pwd) {
                    errorDiv.innerText = "Please enter both email and password";
                    return;
                }
                if (loginUser(email, pwd)) {
                    const modal = bootstrap.Modal.getInstance(document.getElementById("loginModal"));
                    if (modal) modal.hide();
                    loginForm.reset();
                    errorDiv.innerText = "";
                } else {
                    errorDiv.innerText = "Invalid credentials";
                }
            });
        }

        // Logout button
        const logoutBtn = document.getElementById("logoutBtn");
        if (logoutBtn) {
            logoutBtn.addEventListener("click", (e) => {
                e.preventDefault();
                logoutUser();
            });
        }

        // optional: close modals on background click & reset errors
        const modals = ['registerModal', 'loginModal'];
        modals.forEach(modalId => {
            const modalEl = document.getElementById(modalId);
            if (modalEl) {
                modalEl.addEventListener('hidden.bs.modal', function () {
                    if (modalId === 'registerModal') {
                        document.getElementById("registerForm")?.reset();
                        document.getElementById("regEmailError").innerText = "";
                        document.getElementById("regPassError").innerText = "";
                    } else {
                        document.getElementById("loginForm")?.reset();
                        const err = document.getElementById("loginErrorMsg");
                        if (err) err.innerText = "";
                    }
                });
            }
        });
    });