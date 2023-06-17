version 1.0

task request_udn_files {
    meta {
        author: "George Carvalho"
        email: "gcarvalhoneto@mednet.ucla.edu"
        description: "## Task request files from UDN sample"
    }
    parameter_meta {
        api_token_file: {
            description: "TXT with token from UDN gateway API (file-GX6P76j02k8Q5f0QgBV90By0)",
            extension: ".txt"
        }
        udn_id: {
            description: "UDN sample ID (eg.: UDN970218)"
        }
        docker_image: {
            description: "Docker image for python script (file-GX6VF8002k8qFjv0pvY7k4q0)"
        }
    }
    input {
        String udn_id
        File api_token_file
        String? docker_image
    }
    String actual_docker_image=select_first([docker_image, "gvcn/request_udn_files:v0.0.3"])
    command {
        set -uexo pipefail
        python /home/bin/request_udn_files.py -a ~{api_token_file} -u ~{udn_id}
    }
    runtime {
        docker: actual_docker_image
        dx_instance_type: "mem1_ssd1_v2_x16"
        dx_ignore_reuse: true
        dx_restart: object {
            default: 1,
            max: 1,
            errors: object {
                UnresponsiveWorker: 2,
                ExecutionError: 2,
            }
        }
        dx_timeout: "10H30M"
        dx_access: object {
            network: ["*"],
            developer: true
        }
    }
    output {
        Array[File] und_files = glob("*")
    }
}

workflow request_udn_files_wf {
    input {
        String udn_id
        File api_token_file
        String? docker_image
    }
    call request_udn_files {
        input:
            udn_id=udn_id,
            api_token_file=api_token_file,
            docker_image=docker_image
    }
    output {
        Array[File] und_files = request_udn_files.und_files
    }
}