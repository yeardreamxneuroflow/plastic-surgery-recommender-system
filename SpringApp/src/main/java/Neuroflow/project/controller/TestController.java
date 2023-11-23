package Neuroflow.project.controller;

import Neuroflow.project.service.WebClientTest;
import org.apache.commons.io.IOUtils;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.servlet.ModelAndView;

import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.sql.SQLException;
import java.util.Arrays;
import java.util.Base64;

@Controller
@RequestMapping("test")
public class TestController {

    private final WebClientTest webClientTest;

    public TestController(WebClientTest webClientTest) {
        this.webClientTest = webClientTest;
    }

    @GetMapping("/form")
    public String getForm(){
        return "/testTemplate";
    }

    @PostMapping("/input")
    public String sendPost(final Model model, @RequestParam("image") MultipartFile multipartFile) throws IOException, SQLException {

        byte[] imageData = webClientTest.verification(multipartFile);

        String base64ImageData = Base64.getEncoder().encodeToString(imageData);


        model.addAttribute("image_file", base64ImageData);

        return "/image";
    }

}
