package com.feedpulse.twister

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.Button
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp

@Composable
fun Menu(configManager: ConfigManager) {

    var configList by remember { mutableStateOf<List<Setting>>(emptyList()) }

    LaunchedEffect(Unit) {
        // Make the network call and update the state
        val config = configManager.getCurrentConfig()
        configList = config.settingsList
    }

    val context = LocalContext.current
    LazyColumn(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        // Header section
        item {
            Row {
                Spacer(modifier = Modifier.height(4.dp))
                Text(
                    text = "Twister",
                    style = MaterialTheme.typography.headlineMedium,
                )
            }
        }

        // List of settings
        items(configList) { setting ->
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.Start // Aligns items on both ends
            ) {
                Text(
                    setting.prettyName,
                    modifier = Modifier.align(Alignment.CenterVertically),
                )
            }

            Spacer(modifier = Modifier.width(8.dp))

            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.Center
            ) {
                DropdownInput(setting)
            }
        }

        // Apply button
        item {
            Spacer(modifier = Modifier.height(16.dp))
            Button(
                onClick = {
                    configManager.applyChanges(Config(configList), context)
                },
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("Apply Changes")
            }
        }
    }
}
