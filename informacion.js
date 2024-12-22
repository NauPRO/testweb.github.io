const languageTexts = {
    es: {
        intro: "Bienvenido a nuestra aplicación.",
        featuresTitle: "Características",
        feature1Title: "Funcionalidad rápida",
        feature1Description: "Nuestra aplicación es súper rápida y confiable.",
        feature2Title: "Interfaz amigable",
        feature2Description: "Diseñada para ser intuitiva y fácil de usar.",
        feature3Title: "Compatible con todos los dispositivos",
        feature3Description: "Funciona perfectamente en cualquier plataforma.",
        updatesTitle: "Novedades",
        update1Title: "Nueva función agregada",
        update1Description: "Disfruta de la nueva funcionalidad para mejorar tu experiencia.",
        update2Title: "Corrección de errores",
        update2Description: "Mejoras en la estabilidad y rendimiento.",
        downloadTitle: "Compra la aplicación",
        downloadDescription: "Compra nuestra aplicación para desbloquear todo su potencial.",
        downloadBtn: "Comprar"
    },
    en: {
        intro: "Welcome to our app.",
        featuresTitle: "Features",
        feature1Title: "Fast Functionality",
        feature1Description: "Our app is super fast and reliable.",
        feature2Title: "User-Friendly Interface",
        feature2Description: "Designed to be intuitive and easy to use.",
        feature3Title: "Cross-Device Compatibility",
        feature3Description: "Works seamlessly on any platform.",
        updatesTitle: "What's New",
        update1Title: "New Feature Added",
        update1Description: "Enjoy the new functionality to enhance your experience.",
        update2Title: "Bug Fixes",
        update2Description: "Improvements in stability and performance.",
        downloadTitle: "Buy the app",
        downloadDescription: "Purchase our app to unlock its full potential.",
        downloadBtn: "Buy"
    },
    pt: {
        intro: "Bem-vindo ao nosso aplicativo.",
        featuresTitle: "Características",
        feature1Title: "Funcionalidade rápida",
        feature1Description: "Nosso aplicativo é super rápido e confiável.",
        feature2Title: "Interface amigável",
        feature2Description: "Projetado para ser intuitivo e fácil de usar.",
        feature3Title: "Compatível com todos os dispositivos",
        feature3Description: "Funciona perfeitamente em qualquer plataforma.",
        updatesTitle: "Novidades",
        update1Title: "Nova funcionalidade adicionada",
        update1Description: "Aproveite a nova funcionalidade para melhorar sua experiência.",
        update2Title: "Correção de bugs",
        update2Description: "Melhorias na estabilidade e desempenho.",
        downloadTitle: "Compre o aplicativo",
        downloadDescription: "Compre nosso aplicativo para desbloquear todo o seu potencial.",
        downloadBtn: "Comprar"
    }
};

function changeLanguage(language) {
    const texts = languageTexts[language];
    if (!texts) {
        console.error(`No translations found for language: ${language}`);
        return;
    }

    document.getElementById("intro").textContent = texts.intro;
    document.getElementById("features-title").textContent = texts.featuresTitle;
    document.getElementById("feature1-title").textContent = texts.feature1Title;
    document.getElementById("feature1-description").textContent = texts.feature1Description;
    document.getElementById("feature2-title").textContent = texts.feature2Title;
    document.getElementById("feature2-description").textContent = texts.feature2Description;
    document.getElementById("feature3-title").textContent = texts.feature3Title;
    document.getElementById("feature3-description").textContent = texts.feature3Description;
    document.getElementById("updates-title").textContent = texts.updatesTitle;
    document.getElementById("update1-title").textContent = texts.update1Title;
    document.getElementById("update1-description").textContent = texts.update1Description;
    document.getElementById("update2-title").textContent = texts.update2Title;
    document.getElementById("update2-description").textContent = texts.update2Description;
    document.getElementById("download-title").textContent = texts.downloadTitle;
    document.getElementById("download-description").textContent = texts.downloadDescription;
    document.getElementById("download-btn").textContent = texts.downloadBtn;
}

// Agregamos un evento al selector de idiomas
document.addEventListener("DOMContentLoaded", () => {
    const languageSelector = document.getElementById("language-selector");
    languageSelector.addEventListener("change", (event) => {
        const selectedLanguage = event.target.value;
        changeLanguage(selectedLanguage);
    });
});
