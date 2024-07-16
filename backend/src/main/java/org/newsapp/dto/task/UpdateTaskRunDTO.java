package org.newsapp.dto.task;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import org.newsapp.domain.task.TaskRunStatus;

@NoArgsConstructor
@AllArgsConstructor
@Getter
public class UpdateTaskRunDTO {
    private TaskRunStatus status;
    private Long success;
    private Long failed;
}
