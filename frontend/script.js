// ==========================================
// SECTIONS
// ==========================================

const homeSection =
    document.getElementById("homeSection");

const passwordSection =
    document.getElementById("passwordSection");

const emailSection =
    document.getElementById("emailSection");

const generatorSection =
    document.getElementById("generatorSection");

const aboutSection =
    document.getElementById("aboutSection");


// ==========================================
// NAVIGATION
// ==========================================

const homeLink =
    document.getElementById("homeLink");

const aboutLink =
    document.getElementById("aboutLink");

const passwordButton =
    document.getElementById("passwordButton");

const emailButton =
    document.getElementById("emailButton");

const generatorButton =
    document.getElementById("generatorButton");


function hideAllSections() {

    homeSection.classList.add("hidden");

    passwordSection.classList.add("hidden");

    emailSection.classList.add("hidden");

    generatorSection.classList.add("hidden");

    aboutSection.classList.add("hidden");
}


function showHome() {

    hideAllSections();

    homeSection.classList.remove("hidden");

    window.scrollTo(0, 0);
}


// ==========================================
// ACCUEIL
// ==========================================

homeLink.addEventListener(
    "click",
    function (event) {

        event.preventDefault();

        showHome();
    }
);


// ==========================================
// A PROPOS
// ==========================================

aboutLink.addEventListener(
    "click",
    function (event) {

        event.preventDefault();

        hideAllSections();

        aboutSection.classList.remove("hidden");

        window.scrollTo(0, 0);
    }
);


// ==========================================
// PASSWORD CHECKER
// ==========================================

passwordButton.addEventListener(
    "click",
    function () {

        hideAllSections();

        passwordSection.classList.remove(
            "hidden"
        );

        window.scrollTo(0, 0);
    }
);


// ==========================================
// EMAIL CHECKER
// ==========================================

emailButton.addEventListener(
    "click",
    function () {

        hideAllSections();

        emailSection.classList.remove(
            "hidden"
        );

        window.scrollTo(0, 0);
    }
);


// ==========================================
// GENERATEUR
// ==========================================

generatorButton.addEventListener(
    "click",
    function () {

        hideAllSections();

        generatorSection.classList.remove(
            "hidden"
        );

        window.scrollTo(0, 0);
    }
);


// ==========================================
// RETOUR
// ==========================================

document
    .getElementById("backFromPassword")
    .addEventListener(
        "click",
        showHome
    );


document
    .getElementById("backFromEmail")
    .addEventListener(
        "click",
        showHome
    );


document
    .getElementById("backFromGenerator")
    .addEventListener(
        "click",
        showHome
    );


document
    .getElementById("backFromAbout")
    .addEventListener(
        "click",
        showHome
    );


// ==========================================
// AFFICHER / MASQUER PASSWORD
// ==========================================

const passwordInput =
    document.getElementById(
        "passwordInput"
    );

const togglePassword =
    document.getElementById(
        "togglePassword"
    );


togglePassword.addEventListener(
    "click",
    function () {

        if (
            passwordInput.type === "password"
        ) {

            passwordInput.type = "text";

            togglePassword.textContent =
                "🙈";

        } else {

            passwordInput.type =
                "password";

            togglePassword.textContent =
                "👁️";
        }
    }
);


// ==========================================
// PASSWORD CHECKER
// ==========================================

const analyzePasswordButton =
    document.getElementById(
        "analyzePassword"
    );


analyzePasswordButton.addEventListener(
    "click",
    async function () {

        const password =
            passwordInput.value;


        if (!password) {

            alert(
                "Veuillez entrer un mot de passe de test."
            );

            return;
        }


        analyzePasswordButton.disabled =
            true;

        analyzePasswordButton.textContent =
            "Analyse en cours...";


        try {

            const response =
                await fetch(
                    "/api/password/check",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({
                            password: password
                        })
                    }
                );


            const data =
                await response.json();


            if (!response.ok) {

                throw new Error(
                    data.error ||
                    "Une erreur est survenue."
                );
            }


            // ----------------------------------
            // RESULTAT GENERAL
            // ----------------------------------

            document
                .getElementById(
                    "passwordResult"
                )
                .classList.remove(
                    "hidden"
                );


            document
                .getElementById(
                    "scoreValue"
                )
                .textContent =
                String(data.score);


            document
                .getElementById(
                    "securityLevel"
                )
                .textContent =
                String(data.level);


            const score =
                Number(data.score);


            if (
                Number.isFinite(score) &&
                score >= 0 &&
                score <= 100
            ) {

                document
                    .getElementById(
                        "scoreProgress"
                    )
                    .style.width =
                    `${score}%`;

            } else {

                document
                    .getElementById(
                        "scoreProgress"
                    )
                    .style.width =
                    "0%";
            }


            // ----------------------------------
            // PROBLEMES
            // ----------------------------------

            const problemsList =
                document.getElementById(
                    "problemsList"
                );


            problemsList.replaceChildren();


            if (
                !Array.isArray(data.problems) ||
                data.problems.length === 0
            ) {

                const item =
                    document.createElement(
                        "li"
                    );

                item.textContent =
                    "✅ Aucun problème évident détecté.";

                problemsList.appendChild(
                    item
                );

            } else {

                data.problems.forEach(
                    function (problem) {

                        const item =
                            document.createElement(
                                "li"
                            );

                        item.textContent =
                            String(problem);

                        problemsList.appendChild(
                            item
                        );
                    }
                );
            }


            // ----------------------------------
            // RECOMMANDATIONS
            // ----------------------------------

            const recommendationsList =
                document.getElementById(
                    "recommendationsList"
                );


            recommendationsList.replaceChildren();


            if (
                Array.isArray(data.recommendations)
            ) {

                data.recommendations.forEach(
                    function (recommendation) {

                        const item =
                            document.createElement(
                                "li"
                            );

                        item.textContent =
                            String(recommendation);

                        recommendationsList.appendChild(
                            item
                        );
                    }
                );
            }


            // ----------------------------------
            // HIBP
            // ----------------------------------

            const breachResult =
                document.getElementById(
                    "breachResult"
                );


            breachResult.replaceChildren();


            if (data.pwned === true) {

                breachResult.style.border =
                    "1px solid #ff4058";

                breachResult.style.background =
                    "rgba(255,64,88,0.10)";


                const title =
                    document.createElement(
                        "h3"
                    );

                title.textContent =
                    "🚨 Mot de passe compromis";


                const description =
                    document.createElement(
                        "p"
                    );

                description.textContent =
                    "Ce mot de passe apparaît dans des fuites de données connues.";


                const occurrences =
                    document.createElement(
                        "p"
                    );


                const strong =
                    document.createElement(
                        "strong"
                    );

                strong.textContent =
                    "Occurrences :";


                const count =
                    Number(
                        data.breach_count
                    );


                occurrences.appendChild(
                    strong
                );

                occurrences.appendChild(
                    document.createTextNode(
                        Number.isFinite(count)
                            ? ` ${count.toLocaleString("fr-FR")}`
                            : " 0"
                    )
                );


                const warning =
                    document.createElement(
                        "p"
                    );

                warning.textContent =
                    "⚠️ N'utilisez pas ce mot de passe pour un compte important.";


                breachResult.appendChild(
                    title
                );

                breachResult.appendChild(
                    description
                );

                breachResult.appendChild(
                    occurrences
                );

                breachResult.appendChild(
                    warning
                );

            } else {

                breachResult.style.border =
                    "1px solid #52e39b";

                breachResult.style.background =
                    "rgba(82,227,155,0.08)";


                const title =
                    document.createElement(
                        "h3"
                    );

                title.textContent =
                    "🟢 Aucune fuite connue détectée";


                const description =
                    document.createElement(
                        "p"
                    );

                description.textContent =
                    "Ce mot de passe n'a pas été trouvé dans les données de fuites vérifiées.";


                const information =
                    document.createElement(
                        "p"
                    );

                information.textContent =
                    "Cela ne garantit pas qu'il n'a jamais été compromis.";


                breachResult.appendChild(
                    title
                );

                breachResult.appendChild(
                    description
                );

                breachResult.appendChild(
                    information
                );
            }


        } catch (error) {

            // Ne jamais afficher le contenu
            // du mot de passe dans la console.

            alert(
                error instanceof Error
                    ? error.message
                    : "Impossible d'effectuer l'analyse."
            );

        } finally {

            analyzePasswordButton.disabled =
                false;

            analyzePasswordButton.textContent =
                "🔎 Analyser le mot de passe";
        }
    }
);


// ==========================================
// EMAIL CHECKER
// ==========================================

const checkEmailButton =
    document.getElementById(
        "checkEmail"
    );


checkEmailButton.addEventListener(
    "click",
    async function () {

        const emailInput =
            document.getElementById(
                "emailInput"
            );


        const email =
            emailInput.value.trim();


        const result =
            document.getElementById(
                "emailResult"
            );


        const title =
            document.getElementById(
                "emailResultTitle"
            );


        const message =
            document.getElementById(
                "emailResultMessage"
            );


        if (!email) {

            alert(
                "Veuillez entrer une adresse e-mail."
            );

            return;
        }


        checkEmailButton.disabled =
            true;

        checkEmailButton.textContent =
            "Vérification en cours...";


        result.classList.remove(
            "hidden"
        );


        try {

            const response =
                await fetch(
                    "/api/email/check",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({
                            email: email
                        })
                    }
                );


            const data =
                await response.json();


            if (!response.ok) {

                throw new Error(
                    data.error ||
                    "Une erreur est survenue."
                );
            }


            if (
                data.found === true &&
                Array.isArray(data.breaches) &&
                data.breaches.length > 0
            ) {

                title.textContent =
                    "🚨 Adresse trouvée dans des violations";


                message.replaceChildren();


                const description =
                    document.createElement(
                        "p"
                    );

                description.textContent =
                    "Cette adresse apparaît dans des violations de données connues.";


                const countText =
                    document.createElement(
                        "p"
                    );


                const strong =
                    document.createElement(
                        "strong"
                    );

                strong.textContent =
                    "Nombre de violations :";


                countText.appendChild(
                    strong
                );

                countText.appendChild(
                    document.createTextNode(
                        ` ${data.breaches.length}`
                    )
                );


                const list =
                    document.createElement(
                        "ul"
                    );


                data.breaches.forEach(
                    function (breach) {

                        if (
                            !breach ||
                            typeof breach !== "object"
                        ) {
                            return;
                        }


                        const item =
                            document.createElement(
                                "li"
                            );


                        const name =
                            breach.name ||
                            "Violation inconnue";


                        const domain =
                            breach.domain ||
                            "Domaine inconnu";


                        const date =
                            breach.breach_date ||
                            "Date inconnue";


                        item.textContent =
                            `${String(name)} — ${String(domain)} — ${String(date)}`;


                        list.appendChild(
                            item
                        );
                    }
                );


                message.appendChild(
                    description
                );

                message.appendChild(
                    countText
                );

                message.appendChild(
                    list
                );


            } else {

                title.textContent =
                    "🟢 Aucune violation connue détectée";


                message.textContent =
                    "Cette adresse n'a pas été trouvée dans les violations vérifiées par HIBP.";
            }


        } catch (error) {

            title.textContent =
                "❌ Erreur";


            message.textContent =
                error instanceof Error
                    ? error.message
                    : "Impossible d'effectuer la vérification.";

        } finally {

            checkEmailButton.disabled =
                false;

            checkEmailButton.textContent =
                "🔎 Vérifier l'e-mail";
        }
    }
);


// ==========================================
// GENERATEUR
// ==========================================

const passwordLength =
    document.getElementById(
        "passwordLength"
    );


const passwordLengthValue =
    document.getElementById(
        "passwordLengthValue"
    );


const generatePasswordButton =
    document.getElementById(
        "generatePassword"
    );


const generatedPassword =
    document.getElementById(
        "generatedPassword"
    );


const copyPassword =
    document.getElementById(
        "copyPassword"
    );


passwordLength.addEventListener(
    "input",
    function () {

        passwordLengthValue.textContent =
            passwordLength.value;
    }
);


// ==========================================
// GENERER PASSWORD
// ==========================================

generatePasswordButton.addEventListener(
    "click",
    async function () {

        const length =
            Number(
                passwordLength.value
            );


        const useLowercase =
            document.getElementById(
                "useLowercase"
            ).checked;


        const useUppercase =
            document.getElementById(
                "useUppercase"
            ).checked;


        const useDigits =
            document.getElementById(
                "useDigits"
            ).checked;


        const useSpecial =
            document.getElementById(
                "useSpecial"
            ).checked;


        if (
            !useLowercase &&
            !useUppercase &&
            !useDigits &&
            !useSpecial
        ) {

            alert(
                "Sélectionnez au moins un type de caractère."
            );

            return;
        }


        generatePasswordButton.disabled =
            true;

        generatePasswordButton.textContent =
            "Génération...";


        try {

            const response =
                await fetch(
                    "/api/password/generate",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({

                            length: length,

                            use_lowercase:
                                useLowercase,

                            use_uppercase:
                                useUppercase,

                            use_digits:
                                useDigits,

                            use_special:
                                useSpecial
                        })
                    }
                );


            const data =
                await response.json();


            if (!response.ok) {

                throw new Error(
                    data.error ||
                    "Impossible de générer le mot de passe."
                );
            }


            generatedPassword.value =
                data.password;


        } catch (error) {

            alert(
                error instanceof Error
                    ? error.message
                    : "Impossible de générer le mot de passe."
            );


        } finally {

            generatePasswordButton.disabled =
                false;

            generatePasswordButton.textContent =
                "🎲 Générer";
        }
    }
);


// ==========================================
// COPIER
// ==========================================

copyPassword.addEventListener(
    "click",
    async function () {

        if (!generatedPassword.value) {

            alert(
                "Générez d'abord un mot de passe."
            );

            return;
        }


        try {

            await navigator.clipboard.writeText(
                generatedPassword.value
            );


            copyPassword.textContent =
                "✅ Copié !";


            setTimeout(
                function () {

                    copyPassword.textContent =
                        "📋 Copier";

                },
                1500
            );


        } catch (error) {

            alert(
                "Impossible de copier le mot de passe."
            );
        }
    }
);