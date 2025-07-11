package com.feedpulse.twister

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import com.feedpulse.twister.ui.theme.TwisterTheme
import java.net.URL

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            TwisterTheme {
                Menu(
                    ConfigManager(
                        URL("https://feedpulse.francecentral.cloudapp.azure.com/config")
                    )
                )
            }
        }
    }
}
