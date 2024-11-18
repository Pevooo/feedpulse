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
                Menu(ConfigManager(URL("http://10.0.2.2:5000/config")))
            }
        }
    }
}
