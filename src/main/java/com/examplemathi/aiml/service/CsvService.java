package com.examplemathi.aiml.service;

import com.examplemathi.aiml.model.Crop;
import com.opencsv.CSVReader;
import org.springframework.core.io.ClassPathResource;
import org.springframework.stereotype.Service;

import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;

@Service
public class CsvService {

    private final String csvFilePath = "seed_data.csv"; // file inside src/main/resources

    public List<Crop> getAllCrops() {
    List<Crop> crops = new ArrayList<>();
    try {
        ClassPathResource resource = new ClassPathResource(csvFilePath);
        try (CSVReader reader = new CSVReader(new InputStreamReader(resource.getInputStream()))) {
            String[] line;
            boolean firstLine = true;
            while ((line = reader.readNext()) != null) {
                if (firstLine) { firstLine = false; continue; }

                String cropName = line.length > 1 ? line[1] : "";
                String soilType = line.length > 2 ? line[2] : "";
                String duration = line.length > 3 ? line[3] : "";
                String season = line.length > 4 ? line[4] : "";

                String nNeed = "", pNeed = "", kNeed = "";
                if (line.length > 5 && line[5] != null && !line[5].isEmpty()) {
                    String[] npk = line[5].split("-");
                    nNeed = npk.length > 0 ? npk[0] : "";
                    pNeed = npk.length > 1 ? npk[1] : "";
                    kNeed = npk.length > 2 ? npk[2] : "";
                }

                String urea = line.length > 6 ? line[6] : "";
                String dap = line.length > 7 ? line[7] : "";
                String mop = line.length > 8 ? line[8] : "";
                String fertilizerTiming = line.length > 9 ? line[9] : "";
                String avgWater = line.length > 10 ? line[10] : "";
                String extraTips = line.length > 11 ? line[11] : "";
                String harvestingTips = line.length > 12 ? line[12] : "";

                crops.add(new Crop(cropName, duration, season, soilType, avgWater,
                        nNeed, pNeed, kNeed, urea, dap, mop, fertilizerTiming,
                        extraTips, harvestingTips));
            }
        }
    } catch (Exception e) {
        e.printStackTrace();
    }
    return crops;
}


    public List<List<String>> search(String cropFilter, String soilFilter, String seasonFilter) {
        List<List<String>> results = new ArrayList<>();
        for (Crop crop : getAllCrops()) {
            boolean matchesCrop = cropFilter.isEmpty() || crop.getCrop().toLowerCase().contains(cropFilter.toLowerCase());
            boolean matchesSoil = soilFilter.isEmpty() || crop.getSoilType().toLowerCase().contains(soilFilter.toLowerCase());
            boolean matchesSeason = crop.getSeason().toLowerCase().contains(seasonFilter.toLowerCase());

            if (matchesCrop && matchesSoil && matchesSeason) {
                List<String> row = new ArrayList<>();
                row.add(crop.getCrop());
                row.add(crop.getDuration());
                row.add(crop.getSeason());
                row.add(crop.getSoilType());
                row.add(crop.getAvgWater());
                row.add(crop.getnNeed());
                row.add(crop.getpNeed());
                row.add(crop.getkNeed());
                row.add(crop.getUrea());
                row.add(crop.getDap());
                row.add(crop.getMop());
                row.add(crop.getFertilizerTiming());
                row.add(crop.getExtraTips());
                row.add(crop.getHarvestingTips());
                results.add(row);
            }
        }
        return results;
    }
}
