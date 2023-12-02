package Neuroflow.project.controller;

import Neuroflow.project.service.WebClientService;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.sql.SQLException;
import java.util.Base64;

@Controller
@RequestMapping("test")
public class TestController {

    private final WebClientService webClientService;

    public TestController(WebClientService webClientService) {
        this.webClientService = webClientService;
    }

    @GetMapping("/form")
    public String getForm(){
        return "/testTemplate";
    }

    @PostMapping("/input")
    public String sendPost(final Model model, @RequestParam("image") MultipartFile multipartFile) throws IOException, SQLException {

        byte[] imageData = webClientService.verification(multipartFile);

        String base64ImageData = Base64.getEncoder().encodeToString(imageData);


        model.addAttribute("image_file", base64ImageData);

        return "/image";
    }

}
