package com.feedpulse.twister

import android.os.Bundle
import android.util.Log
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.material3.Button
import androidx.compose.material3.DropdownMenu
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Switch
import androidx.compose.material3.Text
import androidx.compose.material3.TextField
import androidx.compose.runtime.Composable
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.feedpulse.twister.ui.theme.TwisterTheme
import java.net.URL

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            TwisterTheme {
                    FeatureSwitch(ConfigManager(URL("http://abc.abc.abc/")))
            }
        }
    }
}

@Composable
fun TextInputExample() {
    // State to hold the input text
    var text by remember { mutableStateOf("") }

    TextField(
        value = text,
        onValueChange = { newText ->
            text = newText  // Update text state with new input
        },
        label = { Text("Enter text here") },
        modifier = Modifier.fillMaxWidth()
    )
}


@Composable
fun FeatureSwitch(configManager: ConfigManager) {
    var configList by remember { mutableStateOf(configManager.getCurrentConfig().settingsList) }

    var switchStates by remember { mutableStateOf(List(configList.size) { false }) }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        Spacer(modifier = Modifier.height(4.dp))
        Text(
            text = "Twister",
            style = MaterialTheme.typography.headlineMedium,
            modifier = Modifier.align(Alignment.CenterHorizontally),
        )

        Text(
            text = "Features",
            style = MaterialTheme.typography.headlineMedium,
            modifier = Modifier.align(Alignment.Start),
        )


        configList.forEachIndexed { i, value ->
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween // Aligns items on both ends
            ) {
                Text(configList[i].settingName)
                Spacer(modifier = Modifier.width(8.dp))
                if (configList[i].settingType == "bool") {
                    Switch(
                        checked = switchStates[i],
                        onCheckedChange = { isChecked ->

                            switchStates = switchStates.toMutableList().apply {
                                this[i] = isChecked
                            }

                            if (isChecked) {
                                configList = configList.toMutableList().apply {
                                    this[i].settingValue = "true"
                                }
                            } else {
                                configList = configList.toMutableList().apply {
                                    this[i].settingValue = "false"
                                }
                            }
                        },
                    )
                } else {
                    TextInputExample()
                }

            }
        }


        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween
        ) {
            Spacer(modifier = Modifier.height(16.dp))
            Button(
                onClick = {
                    configManager.applyChanges(Config(configList))
                },
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("Apply Changes")
            }
        }
    }
}
