package com.feedpulse.twister
import android.content.Context
import android.os.Handler
import android.os.Looper
import android.widget.Toast
import com.google.gson.Gson
import com.google.gson.reflect.TypeToken
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import java.io.OutputStreamWriter
import java.net.HttpURLConnection
import java.net.URL

class ConfigManager(private val url: URL) {
    fun applyChanges(data: Config, context: Context) {
        val postData = Gson().toJson(data)

        CoroutineScope(Dispatchers.IO).launch {
            val connection = (url.openConnection() as HttpURLConnection).apply {
                requestMethod = "POST"
                setRequestProperty("Content-Type", "application/json")
                doOutput = true
            }

            OutputStreamWriter(connection.outputStream).use { writer ->
                writer.write(postData)
                writer.flush()
            }

            val response = connection.inputStream.bufferedReader().use { it.readText() }
            connection.disconnect()
            Handler(Looper.getMainLooper()).post {
                Toast.makeText(context, response, Toast.LENGTH_SHORT).show()
            }
        }
    }

    suspend fun getCurrentConfig(): Config {
        return withContext(Dispatchers.IO) {
            try {
                val connection = (url.openConnection() as HttpURLConnection).apply {
                    requestMethod = "GET"
                }.also {
                    it.connect()
                }

                if (connection.responseCode == HttpURLConnection.HTTP_OK) {
                    val text = connection.inputStream.bufferedReader().use { it.readText() }
                    val listType = object : TypeToken<MutableList<Setting>>() {}.type
                    val settings: MutableList<Setting> = Gson().fromJson(text, listType)
                    return@withContext Config(settings)
                } else {
                    return@withContext Config(mutableListOf())
                }
            } catch (e: Exception) {
                return@withContext Config(mutableListOf())
            }
        }
    }
}

data class Setting(
    val settingName: String,
    var settingValue: String,
    val prettyName: String,
    val choices: List<String>,
)

data class Config(
    var settingsList: List<Setting>
)
