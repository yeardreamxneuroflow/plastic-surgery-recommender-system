package Neuroflow.project.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@Controller
public class HomeController {


    @GetMapping("index.html")
    public String index(){
        return "index";
    }
}
