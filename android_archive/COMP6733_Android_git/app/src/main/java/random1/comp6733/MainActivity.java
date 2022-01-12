package random1.comp6733;

import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.os.Bundle;
import android.util.Log;

import java.util.ArrayList;
import java.util.List;

public class MainActivity extends AppCompatActivity {
    private final String TAG = "MainActivity";
    private RecyclerView bleDeviceRecyclerView;
    private SensorItemAdapter itemAdapter;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        Log.i(TAG, "entered onCreate()");
        setContentView(R.layout.activity_main);
        // set up sensor item list rendering
        this.bleDeviceRecyclerView = this.findViewById(R.id.bleDeviceRecyclerView);
        this.bleDeviceRecyclerView.setLayoutManager(new LinearLayoutManager(this));

        // setup BLE functionality
        // TODO

        List<SensorItemData> itemData = findSensorItems();
        renderItemAdapter(itemData);
    }

    // -------------------------------------------------------------------------------------------
    private List<SensorItemData> findSensorItems() {
        ArrayList<SensorItemData> dataList = new ArrayList<SensorItemData>();

        // TODO - BLE advertising scan... currently just dummy data
        for (int i = 0; i < 20; i++) {
            SensorItemData data = new SensorItemData(this);
            data.setTitle(Integer.toString(i));
            dataList.add(data);
            Log.i(TAG, String.format("findSensorItems() found: %s", data.getTitle()));
        }

        return dataList;
    }

    void renderItemAdapter(List<SensorItemData> itemData) {
        this.itemAdapter = new SensorItemAdapter(this, itemData);
        this.bleDeviceRecyclerView.setAdapter(this.itemAdapter);
        //Log.i(TAG, "renderItemAdapter() finished");
        Log.i(TAG, String.format("renderItemAdapter() data size: %d, adapter size: %d",
                itemData.size(), itemAdapter.getItemCount()));
    }

    // TODO - button functionality
}

