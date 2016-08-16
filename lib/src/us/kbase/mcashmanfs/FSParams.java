
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
    "pangenome_ref",
    "genomes",
    "classes",
    "runCount"
})
public class FSParams {

    @JsonProperty("workspace_name")
    private java.lang.String workspaceName;
    @JsonProperty("pangenome_ref")
    private java.lang.String pangenomeRef;
    @JsonProperty("genomes")
    private List<String> genomes;
    @JsonProperty("classes")
    private List<String> classes;
    @JsonProperty("runCount")
    private Long runCount;
    private Map<java.lang.String, Object> additionalProperties = new HashMap<java.lang.String, Object>();

    @JsonProperty("workspace_name")
    public java.lang.String getWorkspaceName() {
        return workspaceName;
    }

    @JsonProperty("workspace_name")
    public void setWorkspaceName(java.lang.String workspaceName) {
        this.workspaceName = workspaceName;
    }

    public FSParams withWorkspaceName(java.lang.String workspaceName) {
        this.workspaceName = workspaceName;
        return this;
    }

    @JsonProperty("pangenome_ref")
    public java.lang.String getPangenomeRef() {
        return pangenomeRef;
    }

    @JsonProperty("pangenome_ref")
    public void setPangenomeRef(java.lang.String pangenomeRef) {
        this.pangenomeRef = pangenomeRef;
    }

    public FSParams withPangenomeRef(java.lang.String pangenomeRef) {
        this.pangenomeRef = pangenomeRef;
        return this;
    }

    @JsonProperty("genomes")
    public List<String> getGenomes() {
        return genomes;
    }

    @JsonProperty("genomes")
    public void setGenomes(List<String> genomes) {
        this.genomes = genomes;
    }

    public FSParams withGenomes(List<String> genomes) {
        this.genomes = genomes;
        return this;
    }

    @JsonProperty("classes")
    public List<String> getClasses() {
        return classes;
    }

    @JsonProperty("classes")
    public void setClasses(List<String> classes) {
        this.classes = classes;
    }

    public FSParams withClasses(List<String> classes) {
        this.classes = classes;
        return this;
    }

    @JsonProperty("runCount")
    public Long getRunCount() {
        return runCount;
    }

    @JsonProperty("runCount")
    public void setRunCount(Long runCount) {
        this.runCount = runCount;
    }

    public FSParams withRunCount(Long runCount) {
        this.runCount = runCount;
        return this;
    }

    @JsonAnyGetter
    public Map<java.lang.String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(java.lang.String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public java.lang.String toString() {
        return ((((((((((((("FSParams"+" [workspaceName=")+ workspaceName)+", pangenomeRef=")+ pangenomeRef)+", genomes=")+ genomes)+", classes=")+ classes)+", runCount=")+ runCount)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
