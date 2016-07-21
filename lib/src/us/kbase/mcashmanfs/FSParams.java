
package us.kbase.mcashmanfs;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * <p>Original spec-file type: FSParams</p>
 * <pre>
 * Insert your typespec information here.
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "workspace_name",
    "classes",
    "pangenome_ref"
})
public class FSParams {

    @JsonProperty("workspace_name")
    private String workspaceName;
    @JsonProperty("classes")
    private List<Long> classes;
    @JsonProperty("pangenome_ref")
    private String pangenomeRef;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("workspace_name")
    public String getWorkspaceName() {
        return workspaceName;
    }

    @JsonProperty("workspace_name")
    public void setWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
    }

    public FSParams withWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
        return this;
    }

    @JsonProperty("classes")
    public List<Long> getClasses() {
        return classes;
    }

    @JsonProperty("classes")
    public void setClasses(List<Long> classes) {
        this.classes = classes;
    }

    public FSParams withClasses(List<Long> classes) {
        this.classes = classes;
        return this;
    }

    @JsonProperty("pangenome_ref")
    public String getPangenomeRef() {
        return pangenomeRef;
    }

    @JsonProperty("pangenome_ref")
    public void setPangenomeRef(String pangenomeRef) {
        this.pangenomeRef = pangenomeRef;
    }

    public FSParams withPangenomeRef(String pangenomeRef) {
        this.pangenomeRef = pangenomeRef;
        return this;
    }

    @JsonAnyGetter
    public Map<String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public String toString() {
        return ((((((((("FSParams"+" [workspaceName=")+ workspaceName)+", classes=")+ classes)+", pangenomeRef=")+ pangenomeRef)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
