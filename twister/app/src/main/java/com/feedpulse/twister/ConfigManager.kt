package com.feedpulse.twister
import com.google.gson.Gson
import com.google.gson.reflect.TypeToken
import java.io.OutputStreamWriter
import java.net.HttpURLConnection
import java.net.URL

class ConfigManager(private val url: URL) {

    private var cachedConfig: Config? = null

    fun applyChanges(data: Config) {

        val gson = Gson()
        val postData = gson.toJson(data)

        val connection = (url.openConnection() as HttpURLConnection).apply {
            requestMethod = "POST"
            setRequestProperty("Content-Type", "application/json")
            doOutput = true
        }

        OutputStreamWriter(connection.outputStream).also {
            it.write(postData)
            it.flush()
            it.close()
        }
    }

    fun getCurrentConfig(): Config {
        if (cachedConfig != null) {
            return cachedConfig!!
        }

        return try {
            val connection = (url.openConnection() as HttpURLConnection)
                .apply {
                    requestMethod = "GET"
                }.also {
                    it.connect()
                }

            if (connection.responseCode == HttpURLConnection.HTTP_OK) {
                val text = connection.inputStream.bufferedReader().use { it.readText() }
                val listType = object : TypeToken<MutableList<Setting>>() {}.type
                val settings: MutableList<Setting> = Gson().fromJson(text, listType)
                cachedConfig = Config(settings)
                cachedConfig!!
            } else {
                Config(mutableListOf())
            }
        } catch (e: Exception) {
            Config(mutableListOf())
        }
    }
}

class Setting(
    val settingName: String,
    var settingValue: String,
) {
    val settingType = if (settingValue == "true" || settingValue == "false") "bool" else "text"
}

class Config(
    var settingsList: List<Setting>
)
