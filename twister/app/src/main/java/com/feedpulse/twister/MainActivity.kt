package com.feedpulse.twister

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import com.feedpulse.twister.ui.theme.TwisterTheme
import java.net.URL

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            TwisterTheme {
                Menu(ConfigManager(URL("https://graduation-project-chi.vercel.app/settings")))
            }
        }
    }
}
