package com.feedpulse.twister

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.material3.Button
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Switch
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

@Composable
fun Menu(configManager: ConfigManager) {
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
                Text(
                    configList[i].settingName,
                    modifier = Modifier.align(Alignment.CenterVertically),
                )
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
                    TextInput(configList[i])
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