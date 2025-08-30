// src/lib/fetchWithLang.ts

export async function fetchWithLang(
  url: string,
  options: RequestInit = {}
): Promise<Response> {
  try {
    const lang = localStorage.getItem("agritwin-language") || "en";

    // ✅ Append lang query param properly
    const urlObj = new URL(url, window.location.origin);
    urlObj.searchParams.set("lang", lang);

    const response = await fetch(urlObj.toString(), {
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...(options.headers || {}),
      },
    });

    return response;
  } catch (err) {
    console.error("[fetchWithLang Error]:", err);
    throw err;
  }
}
