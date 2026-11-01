; Shared provider storage for the login script and standalone selector.
; Keep it outside AppData: packaged apps such as Codex redirect that folder,
; making their saved selection invisible to a normal Windows startup process.
ReadDictationProvider() {
    EnvGet, userProfile, USERPROFILE
    if (!userProfile)
        throw Exception("Cannot locate the Windows user profile.")
    providerFile := userProfile . "\.talon-dictation\provider.txt"
    try FileRead, provider, %providerFile%
    catch error {
        ; Only a genuinely absent configuration gets the initial Windows
        ; default. An access/read failure must not silently change provider.
        if (A_LastError = 2 || A_LastError = 3)
            return "windows"
        throw Exception("Cannot read the saved provider.")
    }
    provider := Trim(provider, " `t`r`n")
    if (provider != "wispr" && provider != "windows")
        throw Exception("Select wispr or windows with the provider selector.")
    return provider
}
