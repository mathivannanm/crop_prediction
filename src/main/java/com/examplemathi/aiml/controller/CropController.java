package com.examplemathi.aiml.controller;

import com.examplemathi.aiml.service.CsvService;
import org.apache.poi.ss.usermodel.Row;
import org.apache.poi.ss.usermodel.Sheet;
import org.apache.poi.ss.usermodel.Workbook;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.io.ByteArrayOutputStream;
import java.util.ArrayList;
import java.util.List;

@Controller
public class CropController {

    private final CsvService csvService;
    private List<List<String>> lastSearchResult = new ArrayList<>();

    public CropController(CsvService csvService) {
        this.csvService = csvService;
    }

    @GetMapping("/")
    public String index(Model model) {
        return "index"; // index.html
    }

    @PostMapping("/search")
    public String searchCrop(@RequestParam(required = false) String crop,
                             @RequestParam(required = false) String soil,
                             @RequestParam(required = true) String season,
                             Model model) {

        crop = (crop != null) ? crop.trim() : "";
        soil = (soil != null) ? soil.trim() : "";
        season = (season != null) ? season.trim() : "";

        if (season.isEmpty() || (crop.isEmpty() && soil.isEmpty())) {
            model.addAttribute("errorMsg", "Please enter Season + (Crop or Soil)!");
            return "index";
        }

        List<List<String>> matchedRows = csvService.search(crop, soil, season);

        List<List<String>> rowsWithSerial = new ArrayList<>();
        int serial = 1;
        for (List<String> row : matchedRows) {
            List<String> newRow = new ArrayList<>();
            newRow.add(String.valueOf(serial++)); // S.No
            newRow.addAll(row);
            rowsWithSerial.add(newRow);
        }

        lastSearchResult = rowsWithSerial;
        model.addAttribute("rows", rowsWithSerial);
        return "result";
    }

    @GetMapping("/download")
    public ResponseEntity<byte[]> downloadExcel() {
        if (lastSearchResult == null || lastSearchResult.isEmpty()) {
            return ResponseEntity.badRequest().build();
        }

        try (Workbook workbook = new XSSFWorkbook()) {
            Sheet sheet = workbook.createSheet("Filtered Data");

            String[] headers = {
                    "S.No","Crop","Duration (days)","Season","Soil Type",
                    "Avg Water (%)","N Need (kg/ha)","P2O5 Need (kg/ha)","K2O Need (kg/ha)",
                    "Urea (kg/ha)","DAP (kg/ha)","MOP (kg/ha)","Fertilizer Timing","Extra Tips","Harvesting Tips"
            };

            Row header = sheet.createRow(0);
            for (int i = 0; i < headers.length; i++) header.createCell(i).setCellValue(headers[i]);

            int rowNum = 1;
            for (List<String> rowData : lastSearchResult) {
                Row r = sheet.createRow(rowNum++);
                for (int j = 0; j < rowData.size() && j < headers.length; j++) {
                    r.createCell(j).setCellValue(rowData.get(j));
                }
            }

            ByteArrayOutputStream out = new ByteArrayOutputStream();
            workbook.write(out);
            byte[] bytes = out.toByteArray();

            HttpHeaders respHeaders = new HttpHeaders();
            respHeaders.add(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=filtered-data.xlsx");

            return ResponseEntity.ok()
                    .headers(respHeaders)
                    .contentType(MediaType.APPLICATION_OCTET_STREAM)
                    .body(bytes);

        } catch (Exception e) {
            e.printStackTrace();
            return ResponseEntity.internalServerError().build();
        }
    }
}
